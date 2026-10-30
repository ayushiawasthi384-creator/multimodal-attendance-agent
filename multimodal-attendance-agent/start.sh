#!/bin/bash
echo "======================================================================"
echo "   Multimodal Attendance & Engagement Agent - Classroom Intelligence"
echo "======================================================================"

mkdir -p backend/storage/audio backend/storage/code backend/storage/reports backend/uploads

echo "[1/2] Installing requirements..."
pip install -r backend/requirements.txt -q

echo "[2/2] Starting Flask Application on http://localhost:5000 ..."
echo "Standalone Demo Preview available at: demo_preview/index.html"
cd backend
python app.py
