import sqlite3


# Connect to SQLite and create company.db if it does not already exist.
connection = sqlite3.connect("company.db")

# Create a cursor for executing SQL statements.
cursor = connection.cursor()

# Create the department and employee tables.
cursor.execute("""
	CREATE TABLE IF NOT EXISTS department (
		id INTEGER PRIMARY KEY,
		name TEXT,
		location TEXT
	)
""")

cursor.execute("""
	CREATE TABLE IF NOT EXISTS employee (
		id INTEGER PRIMARY KEY,
		name TEXT,
		deptid INTEGER
	)
""")

# Clear old demo rows so the script always leaves exactly five records per table.
cursor.execute("DELETE FROM employee")
cursor.execute("DELETE FROM department")

# Insert five departments. The Support department will have no employees.
departments = [
	(1, "Human Resources", "Mumbai"),
	(2, "Finance", "Delhi"),
	(3, "Information Technology", "Bengaluru"),
	(4, "Sales", "Chennai"),
	(5, "Support", "Hyderabad"),
]
cursor.executemany(
	"INSERT INTO department (id, name, location) VALUES (?, ?, ?)",
	departments,
)

# Insert five employees. Employee 5 has no matching department.
employees = [
	(1, "Aarav Sharma", 1),
	(2, "Diya Patel", 2),
	(3, "Kabir Singh", 3),
	(4, "Meera Nair", 4),
	(5, "Rohan Das", 99),
]
cursor.executemany(
	"INSERT INTO employee (id, name, deptid) VALUES (?, ?, ?)",
	employees,
)

# Save the inserted records in the database.
connection.commit()

# Fetch and display all employee records.
print("Employees:")
print("ID | Name | DeptID")
cursor.execute("SELECT id, name, deptid FROM employee")
for employee in cursor.fetchall():
	print(f"{employee[0]} | {employee[1]} | {employee[2]}")

print()

# Fetch and display all department records.
print("Departments:")
print("ID | Name | Location")
cursor.execute("SELECT id, name, location FROM department")
for department in cursor.fetchall():
	print(f"{department[0]} | {department[1]} | {department[2]}")

# Find and display employees who work in Human Resources.
print()
print("Employees in Human Resources:")
cursor.execute("""
	SELECT employee.name
	FROM employee
	INNER JOIN department ON employee.deptid = department.id
	WHERE department.name = 'Human Resources'
""")
for employee in cursor.fetchall():
	print(employee[0])

# Close the cursor and database connection.
cursor.close()
connection.close()
