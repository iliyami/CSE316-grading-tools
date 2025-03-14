## **CSE316 Grading Setup Automation Script**
This script automates the process of **grading student repositories** by:
- Cloning the student's GitHub repository using **SSH**.
- Copying a **grading template (`test_file.xlsx`)** into the cloned repo.
- **Filling in grading details** (team name, students, grader info) while **preserving Excel formatting**.
- Automating repository setup for **easy push access**.

---

## **Prerequisites**
Ensure you have the following installed:
- **Python 3.7+**
- **Git** (configured with SSH access)
- Python libraries: `pandas` and `openpyxl`

Install dependencies with:
```sh
pip install -r requirements.txt
```

---

## **Usage**
Run the script with:
```sh
python grading_script.py "<Grader Name>" "<test_file.xlsx>" "<team_grading.xlsx>"
```

### **Arguments**
| Argument | Description |
|----------|------------|
| `<Grader Name>` | The name of the grader (used for filtering). |
| `<test_file.xlsx>` | Path to the test grading template file. |
| `<team_grading.xlsx>` | Path to the Excel file containing student repositories and grading assignments. |

---

## **Expected File Formats**
### **1. Team Grading File (`team_grading.xlsx`)**
This file should contain the following columns:

| Column Name | Description |
|-------------|------------|
| **group_name** | The team name or project group. |
| **Grader Name** | The assigned grader's name. |
| **Grader Email** | The grader’s email address. |
| **roster_identifier** | The student's email in the format `x_y.z@q.d` (from which first and last names are extracted). |
| **student_repository_url** | The HTTP URL of the student’s GitHub repository. |

### **2. Test File (`test_file.xlsx`)**
The grading template should contain placeholders in the first column, such as:

| Column 1 (Title) | Column 2 (Filled by Script) |
|------------------|---------------------------|
| **Team Name:** | (Auto-filled) |
| **Student 1:** | (Auto-filled) |
| **Student 2:** | (Auto-filled) |
| **Grader Name:** | (Auto-filled) |
| **Grader Email:** | (Auto-filled) |

The script finds these labels and inserts the corresponding values in the **next column** while **preserving formatting**.

---

## **How It Works**
1. **Reads the `team_grading.xlsx` file** and filters rows by the specified grader.
2. **Converts the GitHub repo URL from HTTP to SSH** for push access.
3. **Clones each team’s repository** (if not already cloned).
4. **Copies the test grading file (`test_file.xlsx`)** into the cloned repository.
5. **Extracts student names** from `roster_identifier` (email format: `x_y.z@q.d` → First: `y`, Last: `z`).
6. **Fills in the grading template** (team name, students, grader info) in the **next column** while **keeping existing formatting**.
7. **Saves the updated file** inside the cloned repository.

---

## **Example**
```sh
python grading_script.py "Iliya Mirzaei" "grading_template.xlsx" "team_grading.xlsx"
```
### **What Happens?**
- Finds teams graded by **Iliya Mirzaei**.
- Clones each **student repository** using SSH.
- Copies **grading_template.xlsx** into each repo.
- Updates the grading file with team & student details.
- Saves it inside the repo **without changing formatting**.

---

## **Troubleshooting**
### **1. GitHub Authentication Issues**
Make sure your **SSH key is added to GitHub**:
```sh
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-add ~/.ssh/id_rsa
```
Test your SSH connection:
```sh
ssh -T git@github.com
```

### **2. Missing Dependencies**
If the script fails due to missing libraries, install them with:
```sh
pip install pandas openpyxl
```

### **3. Formatting Issues in Excel**
- Ensure your **grading template (`test_file.xlsx`)** is formatted correctly.
- The script **does not modify styles** but only fills in values.

---

## **Contributing**
Feel free to open an issue or submit a pull request if you have improvements!

---

## **License**
This script is open-source under the **MIT License**.

---

## Created by: **Iliya Mirzaei**