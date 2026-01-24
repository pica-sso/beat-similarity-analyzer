# beat-similarity-analyzer

> AI-powered beat similarity and originality analysis platform for beatmakers.

BeatScan is an AI-based service that analyzes how similar a given hip-hop beat is to existing beats, helping beatmakers evaluate originality, detect stylistic overlap, and improve creative decisions.

By combining large-scale YouTube beat data, advanced audio source separation, deep audio embeddings, and vector similarity search, BeatScan aims to become an essential tool for modern beatmakers.

---

## 🎯 Problem Statement

In today’s beatmaking ecosystem:

- Thousands of "type beats" are uploaded daily to YouTube.
- Producers often reuse similar drum kits, 808 patterns, and hi-hat rolls.
- It is increasingly difficult to know whether a beat is truly original or stylistically saturated.

Beatmakers frequently ask:

- Is my beat too similar to existing beats?
- Which producers or tracks does my beat resemble?
- Which part of my beat lacks originality?

BeatScan is designed to answer these questions with data-driven similarity analysis and actionable feedback.

---

## 🧠 Core Idea

BeatScan analyzes **drum and texture similarity** in hip-hop beats by:

- Isolating rhythm and bass components  
- Extracting deep audio embeddings  
- Searching a large vector database of reference beats  
- Reporting similarity scores and creative recommendations  

The system focuses on:

- 808 bassline patterns  
- Hi-hat roll structures  
- Drum groove and rhythm  
- Drum sample timbre and texture  

---

## 🔬 Data Source

### Target Dataset (Initial Phase)

- Source: YouTube  
- Query: `"type beat"`  
- Initial size: Top 1,000 most relevant beats  
- Expansion plan: Incremental dataset growth  

Each beat is stored with:

- YouTube video ID  
- Title and channel metadata  
- Audio file  
- Extracted embeddings  

---

## 🏗️ System Pipeline

### End-to-End Flow

1. **User Upload**
   - User uploads an MP3 beat file.

2. **Source Separation**
   - Demucs separates:
     - Drums
     - Bass
     - (Optional) Other stems

3. **Audio Embedding**
   - Extract features using:
     - CLAP (Contrastive Language-Audio Pretraining)
     - Librosa-based features (MFCC, spectral, rhythm)

4. **Vector Search**
   - Store embeddings in PostgreSQL + pgvector  
   - Perform similarity search against reference beat embeddings  

5. **Result Generation**
   - Retrieve top-K similar beats  
   - Compute similarity scores  
   - Generate visual and textual report  

---

## 🛠️ Tech Stack

### Audio & AI

- **Source Separation**: Demucs  
- **Feature Extraction**: Librosa  
- **Deep Embedding**: CLAP  
- **ML Framework**: PyTorch  

### Backend & Database

- **Backend**: FastAPI  
- **Database**: PostgreSQL  
- **Vector Extension**: pgvector  
- **Similarity Metric**: Cosine similarity / inner product  

### Data & Infrastructure

- **Data Collection**: YouTube crawling  
- **Storage**: Object storage for audio files  
- **Deployment**: Docker, Cloud  

---

## 📊 Similarity Analysis

BeatScan evaluates similarity along multiple dimensions:

- **Drum Pattern Similarity**
- **Hi-hat Roll Structure**
- **808 Bassline Shape**
- **Drum Sample Timbre**
- **Overall Rhythm Texture**

Each query returns:

- Top-N most similar beats  
- Similarity percentage score  
- Direct links to reference beats  
- Visualization of similarity distribution  
- Highlighted segments of high similarity  

---

## 📈 User Report Example

For each uploaded beat, the user receives:

- Overall similarity score (0–100%)  
- List of most similar reference beats  
- Producer and track links  
- Similarity breakdown by:
  - Drums  
  - Bass  
  - Hi-hats  
- Creative feedback, such as:

> “Your drum groove is highly similar (82%) to Track X.  
> Consider introducing a more unique hi-hat pattern in bars 9–16.”

---

## 💡 Advanced Features (Planned)

- **Plagiarism Risk Estimation**
- **Producer Style Profiling**
- **Sample Pack Similarity Detection**
- **Freshness Score** (how novel a beat is within the dataset)
- **Style Overlap Detection between producers**
- **Trend Analysis by era and genre**

---

## 💳 Business Model

BeatScan is designed as a **credit-based service**:

- Users purchase credits  
- Each analysis consumes credits  
- Free trial with limited reports  
- Premium features:
  - Detailed breakdown  
  - Historical tracking  
  - Batch analysis  

Target users:

- Independent beatmakers  
- Professional producers  
- Labels and A&R teams  

---

## 🚀 Vision

BeatScan aims to become:

> **The standard originality and style analysis platform for beatmakers.**

By providing objective similarity metrics and creative feedback, BeatScan helps producers:

- Protect originality  
- Avoid unintentional plagiarism  
- Develop a unique signature sound  

---

## 📁 Project Status

This project is currently in early development.

Initial goals:

- Build YouTube beat dataset  
- Implement Demucs + CLAP pipeline  
- Integrate pgvector similarity search  
- Deliver first working similarity report  

---

## 🤝 Contributing

This is an early-stage research and product development project.  
Discussions, ideas, and collaborations are welcome.

---

## 📄 License

License will be added in a future release.
