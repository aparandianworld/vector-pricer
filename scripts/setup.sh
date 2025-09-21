#!/bin/bash
# Simple Vector Pricer Setup

echo "Vector Pricer Setup..."

# Check we're in the right place
cd "$(dirname "$0")/../"

# Basic .env check
if [ ! -f .env ]; then
    echo "No .env file. Creating basic one..."
    cat > .env << EOF
OPENAI_API_KEY=sk-your-key-here
POSTGRES_URL=sqlite:///data/laptops.db
VECTOR_DB_PATH=faiss_index
EOF
    echo "Edit .env with your OPENAI_API_KEY, then run this again!"
    exit 1
fi

# Quick deps check (skip if already installed)
if ! pip show langchain > /dev/null 2>&1; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Dependencies already installed"
fi

# Create data dir
mkdir -p data

# Generate sample data first
echo "Generating sample data..."
python -m data.scripts.generate_sample_data

# Set up databases
echo "Setting up RDBMS (prices)..."
python -m src.data.db_setup
echo "Setting up VectorDB (features)..."
python -m src.data.vector_ingestion

# Test it
echo "Running tool tests..."
python -m tests.test_tools_quick

echo "Setup done! Your tools are ready."
echo "Next: Run 'python -m tests.test_tools_quick' to see them in action"