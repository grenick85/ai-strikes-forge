// AI STRIKES - Dashboard Controller

document.addEventListener('DOMContentLoaded', () => {
    // Update sync time
    updateSyncTime();
    setInterval(updateSyncTime, 60000);

    // Handle strike form submission
    const strikeForm = document.getElementById('strike-form');
    if (strikeForm) {
        strikeForm.addEventListener('submit', handleStrike);
    }
});

function updateSyncTime() {
    const now = new Date();
    const time = now.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        second: '2-digit' 
    });
    const syncTimeElement = document.getElementById('sync-time');
    if (syncTimeElement) {
        syncTimeElement.textContent = time;
    }
}

async function handleStrike(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    // Get citizen_id from the page
    const citizenName = document.querySelector('.citizen-name strong');
    const citizen_id = citizenName ? citizenName.textContent : 'Unknown';

    formData.append('citizen_id', citizen_id);

    // Show loading state
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ PROCESSING...';

    try {
        const response = await fetch('/strike', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayResults(data);
            
            // Update fusion cores display
            if (data.cost) {
                updateFusionCores(data.cost);
            }
        } else {
            showError('Strike failed: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = originalText;
    }
}

function displayResults(data) {
    const resultsPanel = document.getElementById('results-panel');
    const predictionResult = document.getElementById('prediction-result');

    if (!resultsPanel || !predictionResult) return;

    // Clear previous results
    predictionResult.innerHTML = '';

    if (data.status === 'SUCCESS') {
        const homeScore = data.home_score || 0;
        const awayScore = data.away_score || 0;
        const homeTeam = data.home_team || 'UNKNOWN';
        const awayTeam = data.away_team || 'UNKNOWN';
        const confidence = data.confidence || 'N/A';
        const tier = data.tier || 'Unknown';
        const intel = data.intel || 'Processing...';
        
        // Determine winner
        let winner = '';
        let winnerEmoji = '⚖️';
        if (homeScore > awayScore) {
            winner = `${homeTeam} WINS`;
            winnerEmoji = '🎯';
        } else if (awayScore > homeScore) {
            winner = `${awayTeam} WINS`;
            winnerEmoji = '🎯';
        } else {
            winner = 'DEAD HEAT';
            winnerEmoji = '⚖️';
        }
        
        predictionResult.innerHTML = `
            <div style="margin-bottom: 20px;">
                <h3>🎯 PREDICTION ACQUIRED</h3>
                <p style="color: #00ff41; font-size: 1.1em; font-weight: bold; margin: 15px 0;">
                    ${intel}
                </p>
            </div>

            <div style="background-color: rgba(0, 217, 255, 0.1); border: 2px solid #00d9ff; border-radius: 8px; padding: 20px; margin-bottom: 20px;">
                <h3 style="color: #00d9ff; margin-bottom: 15px;">📊 PREDICTED FINAL SCORE</h3>
                
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; align-items: center;">
                    <div style="text-align: center; background-color: rgba(0, 255, 65, 0.1); padding: 20px; border-radius: 8px; border: 1px solid #00ff41;">
                        <p style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 8px;">HOME</p>
                        <p style="color: #00ff41; font-size: 0.95em; margin-bottom: 5px; font-weight: bold;">${homeTeam}</p>
                        <p style="color: #00ff41; font-size: 2.5em; font-weight: bold;">${homeScore}</p>
                    </div>

                    <div style="text-align: center;">
                        <p style="color: #a0a0a0; font-size: 0.85em; margin-bottom: 8px;">OUTCOME</p>
                        <p style="color: #00d9ff; font-size: 2em;">${winnerEmoji}</p>
                        <p style="color: #00d9ff; font-size: 0.9em; font-weight: bold;">${winner}</p>
                    </div>

                    <div style="text-align: center; background-color: rgba(255, 0, 110, 0.1); padding: 20px; border-radius: 8px; border: 1px solid #ff006e;">
                        <p style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 8px;">AWAY</p>
                        <p style="color: #ff006e; font-size: 0.95em; margin-bottom: 5px; font-weight: bold;">${awayTeam}</p>
                        <p style="color: #ff006e; font-size: 2.5em; font-weight: bold;">${awayScore}</p>
                    </div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px; margin-bottom: 20px;">
                <div style="background-color: rgba(0, 255, 65, 0.05); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px;">
                    <p style="color: #a0a0a0; font-size: 0.85em; margin-bottom: 5px;">Intelligence Tier</p>
                    <p style="color: #00ff41; font-weight: bold;">${tier}</p>
                </div>
                <div style="background-color: rgba(0, 255, 65, 0.05); border: 1px solid var(--border-color); border-radius: 8px; padding: 15px;">
                    <p style="color: #a0a0a0; font-size: 0.85em; margin-bottom: 5px;">Confidence Level</p>
                    <p style="color: #00ff41; font-weight: bold;">${confidence}</p>
                </div>
            </div>

            <div style="background-color: rgba(0, 255, 65, 0.05); border-top: 1px solid rgba(0, 255, 65, 0.3); padding-top: 15px; margin-top: 15px;">
                <p style="color: #00ff41; font-size: 0.9em;">✓ Data encrypted and stored in vault</p>
                <p style="color: #a0a0a0; font-size: 0.85em; margin-top: 5px;">Timestamp: ${new Date().toLocaleString()}</p>
            </div>
        `;
    } else {
        predictionResult.innerHTML = `
            <h3>⚠️ STRIKE INCOMPLETE</h3>
            <p><strong>Status:</strong> ${data.status}</p>
            <p style="color: #ff006e;">${data.detail || 'Unable to acquire intelligence at this time.'}</p>
        `;
    }

    // Show results panel
    resultsPanel.style.display = 'block';

    // Scroll to results
    resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function updateFusionCores(cost) {
    const coresDisplay = document.getElementById('cores-display');
    if (coresDisplay) {
        const currentCores = parseFloat(coresDisplay.textContent);
        const newCores = currentCores - cost;
        coresDisplay.textContent = newCores.toFixed(1);
        
        // Flash animation
        coresDisplay.style.color = '#ff006e';
        setTimeout(() => {
            coresDisplay.style.color = '';
        }, 500);
    }
}

function showError(message) {
    const resultsPanel = document.getElementById('results-panel');
    const predictionResult = document.getElementById('prediction-result');

    if (resultsPanel && predictionResult) {
        predictionResult.innerHTML = `
            <h3>❌ ERROR</h3>
            <p style="color: #ff006e;">${message}</p>
        `;
        resultsPanel.style.display = 'block';
        resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}
