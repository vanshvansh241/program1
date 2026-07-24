# studen management system 
students = []
while True:
    print("/=======student Management system=======/")
    print("1. Add student")
    print("2. View  All students")
    print("3. Search student")
    print("4. Update student")
    print("5. Delete student")
    print("6. Exit")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        # students
        sid = input("Enter student ID: ")
        name = input("Enter student name: ")
        age = int(input("Enter student age: "))
        student = {"ID": sid,"Name": name,"Age": age}
        students.append(student)
        print("Student added successfully!")
    elif choice == 2:
        # view all students
        if len(students) == 0:
            print("No students found.")
        else:
            print("Student List:")
            for student in students:
                print(f"ID: {student['ID']}, Name: {student['Name']}, Age: {student['Age']}")
    elif choice == 3:
        # search student
        search_id = input("Enter student ID to search: ")
        found = False
        for student in students:
            if student['ID'] == search_id:
                print(f"Student found: ID: {student['ID']}, Name: {student['Name']}, Age: {student['Age']}")
                found = True
                break
        if not found:
            print("Student not found.")
    elif choice == 4:
        # update student
        update_id = input("Enter student ID to update: ")
        found = False
        for student in students:
            if student['ID'] == update_id:
                new_name = input("Enter new name: ")
                new_age = int(input("Enter new age: "))
                student['Name'] = new_name
                student['Age'] = new_age
                print("Student updated successfully!")
                found = True
                break
        if not found:
            print("Student not found.")
        elif choice == 5:
            # delete student
            delete_id = input("Enter student ID to delete: ")
            found = False
            for student in students:
                if student['ID'] == delete_id:
                    students.remove(student)
                    print("Student deleted successfully!")
                    found = True
                    break
            if not found:
                print("Student not found.")
    elif choice == 6:
        # exit
        print("Exiting the program.")