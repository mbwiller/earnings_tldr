# EarningsCall-TLDR

An intelligent earnings call analysis platform that transforms complex earnings calls into clear, actionable insights using AI-powered analysis.

## 🚀 Features

### Core Analysis
- **Tier A Analysis**: "Why the Stock Moved" - 4-8 high-level bullets ranked by likely contribution to post-earnings price reaction
- **Tier B Analysis**: "Explain it to Anyone" - Clear, jargon-free summary for non-finance professionals
- **Tier C Analysis**: "For Power Users" - Sophisticated expert digest with quantitative extracts and risk analysis

### Technical Capabilities
- **RAG (Retrieval Augmented Generation)**: Advanced NLP processing with semantic search
- **Document Processing**: Support for PDF, TXT, and DOCX files
- **Market Data Integration**: Yahoo Finance integration for real-time market data
- **PDF Export**: Professional report generation with charts and visualizations
- **Modern Web Interface**: Beautiful, responsive UI built with Tailwind CSS

### Data Sources
- Manual file uploads
- Yahoo Finance integration (real-time)
- Alpha Vantage integration (skeleton ready)
- Sample data for testing

## 🏗️ Architecture

### Backend (FastAPI)
```
server/
├── app/
│   ├── api/                 # API endpoints
│   ├── nlp/                 # NLP processing components
│   │   ├── processor.py     # Transcript processing
│   │   ├── rag_engine.py    # RAG implementation
│   │   └── ...
│   ├── data_providers/      # Market data sources
│   │   ├── yahoo_finance.py # Yahoo Finance integration
│   │   └── ...
│   ├── reporting/           # PDF generation
│   ├── templates/           # Web templates
│   └── config.py           # Configuration
├── main.py                 # FastAPI application
└── requirements.txt        # Python dependencies
```

### Frontend (Integrated)
- **Templates**: Jinja2 templates with Tailwind CSS
- **JavaScript**: Interactive charts and real-time updates
- **Responsive Design**: Mobile-friendly interface

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js (for future frontend development)
- OpenAI API key (optional, for enhanced analysis)

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Earnings-Call-TLDR/earnings-call-tldr
   ```

2. **Setup Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r server/requirements.txt
   ```

3. **Configure environment**
   ```bash
   # Create .env file in server directory
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Start the server**
   ```bash
   cd server
   python main.py
   ```

5. **Access the application**
   - Open http://127.0.0.1:8000 in your browser
   - Upload an earnings call transcript
   - View the comprehensive analysis

## 📊 Usage

### Upload Transcript
1. Navigate to the upload section
2. Select a PDF, TXT, or DOCX file
3. Enter company ticker and period
4. Click "Analyze Transcript"

### Search by Ticker
1. Use the quick analysis section
2. Enter a ticker symbol (e.g., AAPL, MSFT)
3. View available earnings calls
4. Select an analysis to view

### View Analysis Results
The analysis provides three tiers of insights:
- **Tier A**: Key factors affecting stock movement
- **Tier B**: Plain English summary
- **Tier C**: Expert-level analysis with metrics

### Export Reports
- PDF reports are automatically generated
- Include charts, metrics, and comprehensive analysis
- Professional formatting for presentations

## 🔧 Configuration

### Environment Variables
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-4
LLM_TEMPERATURE=0.1

# Server Configuration
SERVER_HOST=127.0.0.1
SERVER_PORT=8000

# Data Providers
YAHOO_FINANCE_ENABLED=true
ALPHA_VANTAGE_ENABLED=false
```

### RAG Settings
```python
MAX_CHUNK_SIZE=1200      # Maximum chunk size for processing
MIN_CHUNK_SIZE=500       # Minimum chunk size
CHUNK_OVERLAP=100        # Overlap between chunks
TOP_K_RETRIEVAL=5        # Number of chunks to retrieve
```

## 🚀 Future Enhancements

### Planned Features
- **Web Scraping**: Social media sentiment analysis
- **Advanced NLP**: Custom financial language models
- **Real-time Analysis**: Live earnings call processing
- **Predictive Analytics**: Stock price impact prediction
- **Multi-modal Analysis**: Audio and visual processing

### Technical Improvements
- **Vector Database**: Pinecone/Weaviate integration
- **Caching**: Redis for performance optimization
- **Monitoring**: Prometheus/Grafana dashboards
- **Scalability**: Microservices architecture

## 📁 Project Structure

```
earnings-call-tldr/
├── server/                 # Backend application
│   ├── app/
│   │   ├── api/           # API endpoints
│   │   ├── nlp/           # NLP components
│   │   ├── data_providers/ # Market data sources
│   │   ├── reporting/     # PDF generation
│   │   └── templates/     # Web templates
│   ├── main.py           # Application entry point
│   └── requirements.txt  # Python dependencies
├── data/                 # Data storage
│   ├── raw/             # Raw transcripts
│   ├── processed/       # Processed data
│   ├── cache/           # Cached data
│   └── reports/         # Generated reports
├── samples/             # Sample data
├── docs/                # Documentation
│   └── future_features/ # Future development plans
└── web/                 # Frontend (Next.js - future)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for informational purposes only and should not be considered as investment advice. Always conduct your own research and consult with financial professionals before making investment decisions.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation in the `docs/` folder
- Review the vision documents for future features

---

**Built with ❤️ using FastAPI, OpenAI, and modern web technologies**
