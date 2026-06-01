# AI Strikes: The Forge 🎯

**A FastAPI-powered AI sports prediction engine with ESPN integration, ELO ratings, and cryptic AI prophecies.**

## 📋 Features

- ✅ **Real-time ESPN Data** - Auto-syncs NCAA/NBA standings and scores
- ✅ **ELO Rating System** - Calculates team strength with home court advantage
- ✅ **Point Differentials** - Tier 2/3 predictions boost using point spread analysis
- ✅ **Fatigue Penalties** - Back-to-back game detection for accuracy
- ✅ **Gemini AI Integration** - Cryptic prophecies for each prediction
- ✅ **Multi-tier System** - Tactical/Eyes/Cyber-nuked prediction levels
- ✅ **User Authentication** - Secure citizen login with fusion core currency
- ✅ **ODS Export** - Download predictions as spreadsheets
- ✅ **Cross-platform** - Works on Windows/Mac/Linux

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# 1. Clone repo
git clone https://github.com/grenick85/ai-strikes-forge.git
cd ai-strikes-forge

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 5. Initialize databases
python seed.py

# 6. Sync ESPN data
python utils/espn_data_loader.py

# 7. Run server
python main.py
```

Server runs at: `http://127.0.0.1:8000/`

## 📊 Architecture

```
ESPN APIs
    ↓
espn_data_loader.py → Fetches standings & scores
    ↓
architect_memory.db → team_stats table
    ↓
model.py → ELO calculations
    ↓
Gemini 2.0 Flash → AI prophecy generation
    ↓
FastAPI endpoints → Return predictions
```

## 🎮 Usage

### Login
1. Navigate to `http://127.0.0.1:8000/`
2. **Citizen ID:** `nicky@ai-strikes.com`
3. **Access Code:** `Vault716`

### Conduct a Strike
1. Select prediction tier:
   - **Tier 1: Tactical Advantage** (0.5 cores) - Basic ELO
   - **Tier 2: Eyes in the Sky** (1.0 cores) - With fatigue penalty
   - **Tier 3: Cyber-nuked** (2.0 cores) - With point differential boost

2. Choose matchup (Home vs Away)
3. View:
   - **Winner prediction**
   - **Confidence percentage**
   - **ELO ratings breakdown**
   - **AI prophecy** (cryptic narrative)

## 📂 Project Structure

```
ai-strikes-forge/
├── main.py                    # FastAPI server
├── model.py                   # Prediction engine
├── seed.py                    # Database initialization
├── requirements.txt           # Dependencies
├── .env.example              # Config template
├── README.md                 # This file
├── utils/
│   ├── __init__.py
│   ├── config.py             # Path & DB management
│   ├── espn_data_loader.py   # ESPN API integration
│   ├── sync_schedule.py      # Schedule sync
│   ├── fatigue_calculator.py # Fatigue detection
│   └── ods_exporter.py       # ODS export
├── static/
│   ├── login.html
│   ├── dashboard.html
│   └── style.css
├── data/
│   ├── nccambrecord.json
│   ├── nccabrank.json
│   └── MATCHUPnccamb.json
├── forge.db                  # User database
└── architect_memory.db       # Predictions & stats
```

## 🔧 Configuration

### Environment Variables (.env)
```env
GEMINI_API_KEY=your_key_here
DEBUG=False
HOST=127.0.0.1
PORT=8000
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Login page |
| POST | `/authenticate` | Authenticate user |
| GET | `/hub/{citizen_id}` | Dashboard |
| POST | `/strike` | Generate prediction |
| GET | `/health` | Health check |

## 🧠 Prediction Algorithm

### ELO Calculation
```python
Base Rating = 1500
Home Rating = Base + (Wins - Losses) * 10 + 100 (home court)
Away Rating = Base + (Wins - Losses) * 10

Win Probability = 1 / (1 + 10^((Away - Home) / 400))
```

### Tier Modifiers
- **Tier 1**: Base ELO only
- **Tier 2**: ELO + 25 point fatigue penalty (B2B games)
- **Tier 3**: ELO + Fatigue + (Point Differential * 10)

## 📝 Logging

All operations are logged to console:
```
[ SCANNING ESPN NCAAB STANDINGS... ]
[ SUCCESS: 357 TEAMS CATALOGED IN MEMORY ]
[ TOP DIFFERENTIALS ]
  Arizona: 23-0 (+12.5 pts)
  Houston: 22-2 (+11.2 pts)
```

## 🐛 Troubleshooting

### "Database locked" error
- Wait 1-2 seconds between script runs
- Only one process should access DB at a time

### ESPN API timeout
- Check internet connection
- ESPN API may be temporarily down
- Retry after 30 seconds

### Gemini API errors
- Verify `GEMINI_API_KEY` in .env
- Check API quota limits
- Ensure API is enabled in Google Cloud Console

## 📦 Dependencies

- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `requests` - HTTP client
- `google-genai` - Gemini AI
- `python-dotenv` - Environment management
- `odfpy` - ODS export (optional)

## 🔐 Security

- ✅ API keys in `.env` (not committed)
- ✅ SQLite databases auto-created
- ✅ User authentication on dashboard
- ✅ Fusion cores prevent spam predictions

## 📈 Next Steps

- [ ] Add prediction accuracy tracking
- [ ] Implement machine learning refinement
- [ ] Add more sports (NFL, NBA, MLB)
- [ ] Deploy to cloud (Heroku, AWS, DigitalOcean)
- [ ] Add WebSocket for real-time updates
- [ ] Build mobile app

## 📄 License

MIT License - See LICENSE file

## 👤 Author

**Nicholas R Green** - [@grenick85](https://github.com/grenick85)

---

**Built with ❤️ for sports prediction enthusiasts**
