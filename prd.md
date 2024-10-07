---

## Product Requirement Document (PRD)

### 1. **Title:**  
**Project Name**: Weekly Finance Tracker  
**Version:** 1.0  
**Date:** [Insert Date]  
**Author(s):** [Name(s)]  
**Approvals:** [Stakeholders]

---

### 2. **Objective:**  
Provide users with a tool that tracks their weekly finances by breaking down their monthly income into manageable categories (savings, expenses, and investments) and visualizes the financial status week-by-week.

---

### 3. **Scope:**

- **Included Features:**
  - Weekly income division
  - Savings, expenses, and investments tracking
  - Responsive UI for visual representation of weekly data
  - Yearly summary based on user inputs
  - Downloadable PDF report for monthly and yearly summaries

- **Excluded Features:**
  - Tax calculation or predictions
  - Integration with external finance APIs

---

### 4. **User Stories:**

- **User Story 1**:  
  *As a user, I want to enter my monthly income so that I can track how much I have in each week.*

  **Inputs:** Monthly income amount  
  **Expected Output:** Automated weekly breakdown into 4 equal parts  

- **User Story 2**:  
  *As a user, I want to categorize my expenses so that I can see where I’m spending most of my income.*

  **Inputs:** Expense category, Amount  
  **Expected Output:** Graphical representation of expense categories per week  

- **User Story 3**:  
  *As a user, I want to save a PDF report of my financial activities for a given month.*

  **Inputs:** Month selection, Data range  
  **Expected Output:** Downloadable PDF file summarizing income, expenses, savings, and investments  

---

### 5. **Functional Requirements:**

1. **Income Management:**
   - Allow users to input their monthly income.
   - Automatically divide income into 4 equal weekly portions.
   - Display a breakdown of weekly budgets.

   **Expected Input**: Monthly Income  
   **Expected Output**: Weekly breakdown displayed on UI.

2. **Expense Tracking:**
   - Users can add expenses under predefined categories (e.g., Food, Transport, Entertainment).
   - Expenses should be deducted from the corresponding weekly budget.
   - Categorized expenses should be visible on a pie chart.

   **Expected Input**: Expense Category, Amount, Week  
   **Expected Output**: Real-time updates to weekly budget and pie chart representation.

3. **Savings & Investment Tracking:**
   - Allow users to allocate a portion of the weekly budget to savings or investments.
   - Show cumulative savings/investments at the end of each month.

   **Expected Input**: Savings/Investment Amount  
   **Expected Output**: Display of updated savings and investments for the month.

4. **PDF Reporting:**
   - Generate monthly and yearly financial summaries.
   - Include charts and tables for income, expenses, and savings.

   **Expected Input**: Date range, Report Type (Monthly/Yearly)  
   **Expected Output**: PDF Report generated with the selected data range.

---

### 6. **Non-Functional Requirements:**

1. **Performance:**  
   - The app should respond to user inputs within 1 second.  
   - PDF generation should complete in under 5 seconds.

2. **Security:**  
   - Store user data locally using encrypted SQLite database.  
   - No sensitive data should be stored in plain text.

3. **Scalability:**  
   - Should handle up to 10,000 users without degradation.  

---

### 7. **Milestones & Timeline:**

- **M1:** UI Design (1 Week)  
  - Task 1: Create wireframes for user input fields  
  - Task 2: Design weekly breakdown display  

- **M2:** Core Functionality Implementation (2 Weeks)  
  - Task 1: Implement monthly income breakdown logic  
  - Task 2: Develop expense tracking module  

- **M3:** Testing & QA (1 Week)  
  - Task 1: Create test cases for each input scenario  
  - Task 2: Conduct usability testing  

---

### 8. **Success Criteria:**  
- 80% of users complete weekly tracking.  
- 60% of users generate monthly PDF reports.  
- Positive user feedback on insights.

---

---
### 9. **GitHub Issue Creation Example:**

**Issue Title:** Implement Monthly Income Breakdown Functionality  
- **Description:** Implement the logic to break down monthly income into 4 equal weekly segments and display them in the UI.
- **Inputs:** Monthly income entered by the user.
- **Expected Output:** Weekly income distribution shown as 4 cards labeled Week 1, Week 2, Week 3, Week 4.
- **Labels:** feature, frontend, backend
- **Assignees:** @developer1, @developer2
- **Attachments:** [Wireframe Mockup](link-to-wireframe), [Design Specifications](link-to-design-doc)

**Issue Title:** Create Pie Chart for Categorized Expenses  
- **Description:** Build a visual component to show expense categories in a pie chart.
- **Inputs:** Expense category, Amount entered by the user for each week.
- **Expected Output:** Real-time pie chart display of categorized expenses for the selected week.
- **Labels:** feature, frontend, data-visualization
- **Assignees:** @developer3
- **Attachments:** [Pie Chart Design](link-to-design), [Expense Categories List](link-to-categories)
---

