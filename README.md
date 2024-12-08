# Data Management for Web App Using Firebase Firestore

This README outlines the data structure, cleaning process, and table generation strategy for integrating Firebase Firestore data into BigQuery for analysis.

---

## **1. Firebase Firestore Data Structure**

### **Collection: `/users`**
Each user document is identified by a unique **User-UUID**. The user data is structured as follows:

#### Example:
**Path:** `/users/{User-UUID}/results`

- **BewussteInkompetenz/answers**  
  Example: `0 = 5`

- **finalCharacter**  
  - `combinedTotalScore`: Total score (e.g., `60`)
  - `completionDate`: Date and time when the final character was completed (e.g., `20 November 2024 at 09:40:11 UTC+1`)
  - `finalCharacter`: Name of the character (e.g., `"Anonymous"`)
  - `finalCharacterDescription`: Description of the final character.

---

### **Collection: `/fragen`**
Each question document includes:

- **backgroundInfo**: Contextual information about the question.
- **Id**: Unique identifier for the question.
- **set**: The set this question belongs to.
- **text**: The question text.
- **value**: Associated score or value.

---

## **2. Data Cleaning Process**

Before exporting data for BigQuery, ensure that:

1. **FinalCharacter Data Validation:**  
   Remove any result entries that lack the `finalCharacter` document or associated fields.

2. **Question Data Validation:**  
   Ensure all `Fragen` entries referenced in user results have a valid `Id`.

---

## **3. BigQuery Table Structure**

To facilitate analysis, the following tables should be generated:

### **3.1 FinalCharacterDoc_[User-UUID_ResultsX]**
This table consolidates data from the `finalCharacter` document for a specific user and result set.

| Column                  | Type       | Description                                   |
|-------------------------|------------|-----------------------------------------------|
| User-UUID               | STRING     | Unique user identifier.                      |
| ResultsX                | STRING     | Results set identifier.                      |
| CombinedTotalScore      | INT64      | Total score for the test.                    |
| CompletionDate          | TIMESTAMP  | Date and time of test completion.            |
| FinalCharacter          | STRING     | Name of the final character.                 |
| FinalCharacterDescription | STRING   | Description of the final character.          |

---

### **3.2 FrageID_[User-UUID_ResultsX]**
This table stores details of the questions answered for a specific user and result set.

| Column    | Type       | Description                                |
|-----------|------------|--------------------------------------------|
| User-UUID | STRING     | Unique user identifier.                   |
| ResultsX  | STRING     | Results set identifier.                   |
| FrageID   | STRING     | Unique identifier for the question.       |
| Answer    | INT64      | User-provided score or value.             |

---

### **3.3 Aggregated Scores**
A summary table to store average scores for various categories:

**Table Name:** `[User-UUID_ResultsX]_AVG_Scores`

| Column                   | Type       | Description                                |
|--------------------------|------------|--------------------------------------------|
| User-UUID                | STRING     | Unique user identifier.                   |
| ResultsX                 | STRING     | Results set identifier.                   |
| AVG-Score-Lebensbereich1 | FLOAT64    | Average score for the first category.     |
| AVG-Score-LebensbereichX | FLOAT64    | Average score for other categories.       |
| AVG-Score-Ebene          | FLOAT64    | Average score across all categories.      |

---

## **4. Trigger Implementation**

### Trigger: **After Test Completion**
1. Monitor for the completion of a test (indicated by a populated `finalCharacter` document).
2. Validate and clean data:
   - Remove incomplete or invalid entries.
3. Export valid data to BigQuery:
   - Populate the above tables.

---

## **5. Automation Flow**

1. **Data Export Pipeline:**
   - Use Firebase Cloud Functions to trigger data export after test completion.
   - Validate the `finalCharacter` and `Fragen` data.

2. **Data Transformation:**
   - Use a processing script or tool (e.g., Python, Dataflow) to generate CSV files in the specified structure.

3. **BigQuery Integration:**
   - Load the generated CSV files into BigQuery for analysis.

---

This setup ensures a clean, structured pipeline from Firestore to BigQuery, supporting robust data analysis.
