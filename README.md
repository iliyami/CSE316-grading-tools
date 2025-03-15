# **📌 Grading Setup Automation Script**

```
    ░▒▓██████▓▒░ ░▒▓███████▓▒░▒▓████████▓▒░      ░▒▓███████▓▒░   ░▒▓█▓▒░░▒▓███████▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░                    ░▒▓█▓▒░▒▓████▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░                    ░▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓██████▓▒░        ░▒▓███████▓▒░   ░▒▓█▓▒░▒▓███████▓▒░  
    ░▒▓█▓▒░             ░▒▓█▓▒░▒▓█▓▒░                    ░▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░      ░▒▓█▓▒░▒▓█▓▒░                    ░▒▓█▓▒░  ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ 
    ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░      ░▒▓███████▓▒░   ░▒▓█▓▒░░▒▓██████▓▒░  
                                                                                   
                            GitHub Repository Grading Automation  
                            👨‍💻 **Created by: Iliya Mirzaei**  
```

## **🔹 Overview**
This script automates the **grading setup** for student repositories in **CSE316** by:  
✅ **Cloning GitHub repositories** using SSH  
✅ **Copying grading templates** into each repository  
✅ **Preserving Excel formatting** while filling in team & student details  
✅ **Extracting commit timestamps** to assess late submissions  
✅ **Applying automatic penalties** based on a **configurable deadline policy**  
✅ **Handling deadline extensions** for specific teams  
✅ **Logging late submissions** in a dedicated `late_submissions.txt` file  

---

## **📥 Installation**
1. **Install Python 3.7+** (if not already installed).  
2. Install dependencies using:  
   ```sh
   pip install -r requirements.txt
   ```
3. Ensure your **SSH key is added to GitHub**:  
   ```sh
   ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
   ssh-add ~/.ssh/id_rsa
   ssh -T git@github.com
   ```

---

## **🚀 Usage**
Run the script with:  
```sh
python grading_script.py "<Grader Name>" "<test_file.xlsx>" "<team_grading.xlsx>" "<Deadline MM-DD-YYYY>" [Grace Period (default: 0 hours - no shifts!)] [extension_file.txt]
```

### **🔹 Arguments**
| Argument | Description |
|----------|------------|
| `<Grader Name>` | The name of the grader (used for filtering). |
| `<test_file.xlsx>` | Path to the test grading template file. |
| `<team_grading.xlsx>` | Path to the file containing student repositories and assignments. |
| `<Deadline MM-DD-YYYY>` | The **official** submission deadline for grading. |
| `[Grace Period]` (optional) | Extra hours (default: **0 hours**) where late penalties **do not apply**. |
| `[extension_file.txt]` (optional) | Path to a file containing team-specific deadline extensions. |

---

## **📑 File Formats**
### **1️⃣ Team Grading File (`team_grading.xlsx`)**
Must contain the following **columns**:

| Column Name | Description |
|-------------|------------|
| **group_name** | The team name or project group. |
| **Grader Name** | The assigned grader's name. |
| **Grader Email** | The grader’s email address. |
| **roster_identifier** | The student’s email in `x_y.z@q.d` format (used for name extraction). |
| **student_repository_url** | The **HTTP** GitHub repository URL (converted to SSH). |

---

### **2️⃣ Test File (`test_file.xlsx`)**
This **grading template** must contain the following placeholders in the first column:

| Column 1 (Title) | Column 2 (Filled by Script) |
|------------------|---------------------------|
| **Team Name:** | (Auto-filled) |
| **Student 1:** | (Auto-filled) |
| **Student 2:** | (Auto-filled) |
| **Grader Name:** | (Auto-filled) |
| **Grader Email:** | (Auto-filled) |

> 📌 **The script fills these values while preserving Excel formatting.**  

---

### **3️⃣ Deadline Extension File (`extension_file.txt`)** _(Optional)_
This file specifies **team-specific deadline extensions** in the following format:

```
Student 1 & Student 2 - My Team, 03/09/2025
```
- The **first part** (`Student 1 & Student 2`) is **for reference only**.  
- The **team name** (`My Team`) **must match** the `group_name` from `team_grading.xlsx`.  
- The **new deadline** (`03/09/2025`) is applied **instead of the original** deadline.

---

## **📊 Late Submission Policy**
🚨 **Penalties are applied based on the last commit timestamp:**  
- **⏳ On time** → **No penalty** (submitted within `[grace period]` after the deadline).  
- **Late (6-30 hours)** → **Max Score: 90%**  
- **Late (30-54 hours)** → **Max Score: 80%**  
- **Late (54-78 hours)** → **Max Score: 70%**  
- **Late (78-102 hours)** → **Max Score: 60%**  
- **Late (102+ hours)** → **Max Score: 50%**  

> 📝 **If a team has an extension,** the **effective deadline** is updated before penalties are applied.

---

## **📂 Late Submission Log (`late_submissions.txt`)**
All late submissions are logged in **`late_submissions.txt`**, including:

✅ **Team Name**  
✅ **Submission Timestamp**  
✅ **Original Deadline & Extension Deadline (if any)**  
✅ **Time Difference from Deadline**  
✅ **Final Submission Status & Score Cap**  

### **📜 Example Log:**
```
📌 Late Submissions Log
--------------------
Team: My Team
   - 🕒 Submission Timestamp: 2025-03-09 15:54:20
   - 📝 Original Deadline: 2025-03-06 00:00:00
   - ⏳ Time Difference: 15.91 hours
   - 🚦 Submission Status: ⏳ Late (90% cap)
   - 🆓 Extension Granted Until: 2025-03-09 00:00:00
   - 🔴 Max Score Capped at 90%
```

---

## **📌 Example Run**
```sh
python grading_script.py "Iliya Mirzaei" "grading_template.xlsx" "team_grading.xlsx" "03-06-2025" 6 "extensions.txt"
```

### **🔹 What Happens?**
✅ Filters teams assigned to **Iliya Mirzaei** TA(Grader) 
✅ Clones **each team's repository**  
✅ Copies and fills in **grading templates**  
✅ Extracts **last commit timestamps**  
✅ Applies **late penalties (if any)**  
✅ Logs **all late submissions** in `late_submissions.txt`  

---

## **🛠️ Troubleshooting**
### **🔹 GitHub SSH Access Issues**
```sh
ssh -T git@github.com
```
If you see **"Permission denied"**, add your SSH key:  
```sh
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
ssh-add ~/.ssh/id_rsa
```

### **🔹 Missing Dependencies?**
```sh
pip install -r requirements.txt
```

---

## **👨‍💻 Contributing**
Feel free to **open an issue** or **submit a pull request** for improvements!  

---

## **📜 License**
This script is **open-source** under the **MIT License**.

---