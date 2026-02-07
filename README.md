# GameMatcher: Actionable Knowledge Representation System

**GameMatcher** is a semantic web project designed to solve the common problem: *"Can my PC run this game?"*. By leveraging Knowledge Graphs, Ontologies (OWL), and Reasoners, the system automatically matches video game system requirements (from Steam) with user hardware specifications (benchmarked via PassMark) to infer compatibility, recommend games, and provide actionable insights.

This project was developed for the **Actionable Knowledge Representation** course.

---

## 📂 Repository Structure

The repository is organized into three main delivery phases:

* **`D1/` (Phase 1):** Domain Analysis & Competency Questions.
    * Initial project proposal and scope definition (`Submission_D1.pdf`).
* **`D2/` (Phase 2):** TBox Implementation (Schema).
    * `gameMatcher_Final.owl`: The core ontology structure (Classes, Properties, Data Properties) without massive data.
    * `GameMacherFinal.ipynb`: Notebook for TBox creation.
* **`D3/` (Phase 3):** ABox Population, Scraping & Reasoning.
    * **`Scraping/`**: Contains Jupyter Notebooks and scripts to scrape data from Steam and PassMark APIs.
        * `cleaning/`: Python scripts for data cleaning, fuzzy matching of hardware names, and parsing unstructured text requirements.
    * **`Ontologies/`**: Contains the populated ontology (`gameMatcher_ABox.owl`) and the inferred version (`gameMatcher_ABoxInferred.owl`).
    * **`GameMatcherwAbox.ipynb`**: The main orchestration notebook that loads data, populates the ontology via `owlready2`, creates synthetic users, and executes the reasoner.
    * **`Queries/`**: SPARQL queries used to validate the system.

---

## 🚀 Key Features

* **Automated Data Pipeline:** Scrapes "Top 100" games from Steam and thousands of CPU/GPU benchmarks from PassMark.
* **Intelligent Parsing:** Uses a custom parser to extract specific hardware models from unstructured text descriptions in Steam system requirements.
* **Semantic Linking Strategy:** Dynamically links user hardware to a standardized catalog of components (Single Source of Truth).
* **Robust Fallback Mechanism:** Automatically handles edge cases by creating "Local Individuals" when a user's hardware is not found in the standard catalog.
* **SWRL Rules & Reasoning:** Utilizes logic rules (e.g., `IF CPU_Score > Req_Score THEN canRun`) to automatically infer compatibility and recommendations.
* **Synthetic User Generation:** Leverages **Gemini 3 Pro** (LLM) to generate realistic test users with diverse hardware profiles using a RAG-based approach.

---

## 🛠️ Installation & Usage

### Prerequisites
* **Python 3.14**
* **Java** (Required for the Pellet/HermiT reasoner to work with `owlready2`)
### 3. Run the Pipeline
The core logic is contained within the `D3` folder.

1.  **Data Collection (Optional):** If you want to refresh the data, run the notebooks in `D3/Scraping/`. *Note: The repo already contains processed JSON files.*
2.  **Ontology Population & Reasoning:** Open and run **`D3/GameMatcherwAbox.ipynb`**.
    * This script loads the JSON data.
    * Creates the ABox (Instances of Games, CPUs, GPUs).
    * Generates synthetic users.
    * Runs the Reasoner to infer `canRun`, `isRecommendedFor`, `isTooExpensiveFor`, etc.
    * Exports the final `.owl` file.

---

## 📊 Data Flow

1.  **Raw Data:** Steam Store (Requirements) + PassMark (Benchmarks).
2.  **Processing:**
    * *Cleaning:* Removal of noise, fuzzy matching of hardware names.
    * *Filtering:* Keeping only relevant hardware to optimize graph size.
3.  **Knowledge Graph:**
    * **TBox:** Classes (`User`, `VideoGame`, `Computer`, `CPU`, `GPU`).
    * **ABox:** Instances (e.g., `User_Marco`, `Game_Cyberpunk2077`, `CPU_Intel_i7`).
4.  **Reasoning:** The system infers relationships like `User_Marco -> canRun -> Game_Cyberpunk2077`.

--
## 👥 Authors

* **Andreea Scrob**
* **Edoardo Tommasi**

---

*Developed with Python, Owlready2, and Protégé.*
