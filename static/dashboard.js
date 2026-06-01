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
        const intel = data.intel;
        
        predictionResult.innerHTML = `
            <h3>🎯 PREDICTION ACQUIRED</h3>
            <p><strong>Status:</strong> ${intel.status || 'UNKNOWN'}</p>
            <p><strong>Intelligence:</strong> ${intel.intel || 'Processing...'}</p>
            <p><strong>Confidence Level:</strong> ${intel.confidence || 'N/A'}</p>
            <div style="margin-top: 15px; padding-top: 15px; border-top: 1px solid rgba(0, 255, 65, 0.3);">
                <p style="color: #00ff41; font-size: 0.9em;">✓ Data encrypted and stored in vault</p>
            </div>
        `;
    } else {
        predictionResult.innerHTML = `
            <h3>⚠️ STRIKE INCOMPLETE</h3>
            <p><strong>Status:</strong> ${data.status}</p>
            <p style="color: #ff006e;">Unable to acquire intelligence at this time.</p>
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