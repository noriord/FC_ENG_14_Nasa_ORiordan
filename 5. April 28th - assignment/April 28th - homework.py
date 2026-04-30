
students = []
teachers = []
homeroom_teachers = []

# students — each has first_name, last_name, class_name
# teachers — each has first_name, last_name, subject, and a classes list
# homeroom_teachers — each has first_name, last_name, class_name

commands = ["create", "manage", "end"]

while True:
    # Show main menu
    print("*" * 40)
    print("What would you like to do?")
    print("*" * 40)
    for i in range(len(commands)):
        print("  {} - {}".format(i + 1, commands[i]))
    print("*" * 40)

    choice = input("Pick a number (1-3): ")

    try:
        number = int(choice)
        if number < 1 or number > 3:
            print("Please pick 1-3.")
            continue
        command = commands[number - 1]
    except ValueError:
        print("Please enter a number.")
        continue

    # ---- CREATE ----
    if command == "create":
        create_commands = ["student", "teacher", "homeroom teacher", "end"]

        while True:
            print("*" * 40)
            print("What type of user to create?")
            print("*" * 40)
            for i in range(len(create_commands)):
                print("  {} - {}".format(i + 1, create_commands[i]))
            print("*" * 40)

            create_choice = input("Pick a number (1-4): ")

            try:
                create_number = int(create_choice)
                if create_number < 1 or create_number > 4:
                    print("Please pick 1-4.")
                    continue
                create_command = create_commands[create_number - 1]
            except ValueError:
                print("Please enter a number.")
                continue

            # -- Create Student --
            if create_command == "student":
                first_name = input("Enter first name: ").strip()
                last_name = input("Enter last name: ").strip()
                class_name = input("Enter class name (e.g. 3C): ").strip()

                if not first_name or not last_name or not class_name:
                    print("All fields are required.")
                    continue

                student = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "class_name": class_name
                }
                students.append(student)
                print("Student '{} {}' added to class '{}'.".format(
                    first_name, last_name, class_name))

            # -- Create Teacher --
            elif create_command == "teacher":
                first_name = input("Enter first name: ").strip()
                last_name = input("Enter last name: ").strip()
                subject = input("Enter subject (e.g. Japanese): ").strip()

                if not first_name or not last_name or not subject:
                    print("All fields are required.")
                    continue

                classes = []
                print("Enter class names one by one (empty line to finish):")
                while True:
                    class_name = input("  Class: ").strip()
                    if class_name == "":
                        break
                    classes.append(class_name)

                if not classes:
                    print("A teacher must teach at least one class.")
                    continue

                teacher = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "subject": subject,
                    "classes": classes
                }
                teachers.append(teacher)
                print("Teacher '{} {}' added for subject '{}', classes: {}.".format(
                    first_name, last_name, subject, classes))

            # -- Create Homeroom Teacher --
            elif create_command == "homeroom teacher":
                first_name = input("Enter first name: ").strip()
                last_name = input("Enter last name: ").strip()
                class_name = input("Enter class name (e.g. 3C): ").strip()

                if not first_name or not last_name or not class_name:
                    print("All fields are required.")
                    continue

                homeroom_teacher = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "class_name": class_name
                }
                homeroom_teachers.append(homeroom_teacher)
                print("Homeroom teacher '{} {}' now leads class '{}'.".format(
                    first_name, last_name, class_name))

            # -- End (back to main menu) --
            elif create_command == "end":
                break

    # ---- MANAGE ----
    elif command == "manage":
        manage_commands = ["class", "student", "teacher", "homeroom teacher", "end"]

        while True:
            print("*" * 40)
            print("What would you like to manage?")
            print("*" * 40)
            for i in range(len(manage_commands)):
                print("  {} - {}".format(i + 1, manage_commands[i]))
            print("*" * 40)

            manage_choice = input("Pick a number (1-5): ")

            try:
                manage_number = int(manage_choice)
                if manage_number < 1 or manage_number > 5:
                    print("Please pick 1-5.")
                    continue
                manage_command = manage_commands[manage_number - 1]
            except ValueError:
                print("Please enter a number.")
                continue

            # -- Manage Class --
            if manage_command == "class":
                print("(Press Enter without typing to see all records)")
                class_name = input("Enter class name (e.g. 3C): ").strip()

                # Show ALL classes
                if class_name == "":
                    if not students and not homeroom_teachers:
                        print("No data in the system yet.")
                        continue

                    all_classes = []
                    for s in students:
                        if s["class_name"] not in all_classes:
                            all_classes.append(s["class_name"])
                    for h in homeroom_teachers:
                        if h["class_name"] not in all_classes:
                            all_classes.append(h["class_name"])

                    print("*" * 40)
                    for c in all_classes:
                        print("Class: {}".format(c))

                        for h in homeroom_teachers:
                            if h["class_name"] == c:
                                print("  Homeroom teacher: {} {}".format(
                                    h["first_name"], h["last_name"]))
                                break

                        for s in students:
                            if s["class_name"] == c:
                                print("  - {} {}".format(s["first_name"], s["last_name"]))
                        print("")
                    print("*" * 40)

                # Show ONE specific class
                else:
                    found_students = []
                    for s in students:
                        if s["class_name"] == class_name:
                            found_students.append(s)

                    found_homeroom = None
                    for h in homeroom_teachers:
                        if h["class_name"] == class_name:
                            found_homeroom = h
                            break

                    if not found_students and found_homeroom is None:
                        print("No data found for class '{}'.".format(class_name))
                        continue

                    print("*" * 40)
                    print("Class: {}".format(class_name))
                    print("*" * 40)

                    if found_homeroom is not None:
                        print("Homeroom teacher: {} {}".format(
                            found_homeroom["first_name"], found_homeroom["last_name"]))
                    else:
                        print("Homeroom teacher: (none assigned)")

                    if found_students:
                        print("Students:")
                        for s in found_students:
                            print("  - {} {}".format(s["first_name"], s["last_name"]))
                    else:
                        print("Students: (none)")
                    print("*" * 40)

            # -- Manage Student --
            elif manage_command == "student":
                print("(Press Enter without typing to see all records)")
                name = input("Enter student's first and last name: ").strip()

                # Show ALL students
                if name == "":
                    if not students:
                        print("No students in the system yet.")
                        continue

                    print("*" * 40)
                    print("All students:")
                    print("*" * 40)
                    for s in students:
                        print("  - {} {} (class: {})".format(
                            s["first_name"], s["last_name"], s["class_name"]))
                    print("*" * 40)

                # Show ONE specific student
                else:
                    parts = name.split()
                    if len(parts) < 2:
                        print("Please enter first and last name.")
                        continue
                    first_name = parts[0]
                    last_name = parts[1]

                    found_student = None
                    for s in students:
                        if s["first_name"] == first_name and s["last_name"] == last_name:
                            found_student = s
                            break

                    if found_student is None:
                        print("Student '{} {}' not found.".format(first_name, last_name))
                        continue

                    student_class = found_student["class_name"]

                    found_teachers = []
                    for t in teachers:
                        if student_class in t["classes"]:
                            found_teachers.append(t)

                    print("*" * 40)
                    print("Student: {} {}".format(first_name, last_name))
                    print("Class: {}".format(student_class))
                    print("*" * 40)

                    if found_teachers:
                        print("Teachers:")
                        for t in found_teachers:
                            print("  - {} {} ({})".format(
                                t["first_name"], t["last_name"], t["subject"]))
                    else:
                        print("Teachers: (none found for this class)")
                    print("*" * 40)

            # -- Manage Teacher --
            elif manage_command == "teacher":
                print("(Press Enter without typing to see all records)")
                name = input("Enter teacher's first and last name: ").strip()

                # Show ALL teachers
                if name == "":
                    if not teachers:
                        print("No teachers in the system yet.")
                        continue

                    print("*" * 40)
                    print("All teachers:")
                    print("*" * 40)
                    for t in teachers:
                        print("  - {} {} | Subject: {} | Classes: {}".format(
                            t["first_name"], t["last_name"], t["subject"], t["classes"]))
                    print("*" * 40)

                # Show ONE specific teacher
                else:
                    parts = name.split()
                    if len(parts) < 2:
                        print("Please enter first and last name.")
                        continue
                    first_name = parts[0]
                    last_name = parts[1]

                    found_teacher = None
                    for t in teachers:
                        if t["first_name"] == first_name and t["last_name"] == last_name:
                            found_teacher = t
                            break

                    if found_teacher is None:
                        print("Teacher '{} {}' not found.".format(first_name, last_name))
                        continue

                    print("*" * 40)
                    print("Teacher: {} {}".format(first_name, last_name))
                    print("Subject: {}".format(found_teacher["subject"]))
                    print("*" * 40)
                    print("Classes:")
                    for c in found_teacher["classes"]:
                        print("  - {}".format(c))
                    print("*" * 40)

            # -- Manage Homeroom Teacher --
            elif manage_command == "homeroom teacher":
                print("(Press Enter without typing to see all records)")
                name = input("Enter homeroom teacher's first and last name: ").strip()

                # Show ALL homeroom teachers
                if name == "":
                    if not homeroom_teachers:
                        print("No homeroom teachers in the system yet.")
                        continue

                    print("*" * 40)
                    print("All homeroom teachers:")
                    print("*" * 40)
                    for h in homeroom_teachers:
                        print("  - {} {} (leads class: {})".format(
                            h["first_name"], h["last_name"], h["class_name"]))
                    print("*" * 40)

                # Show ONE specific homeroom teacher
                else:
                    parts = name.split()
                    if len(parts) < 2:
                        print("Please enter first and last name.")
                        continue
                    first_name = parts[0]
                    last_name = parts[1]

                    found_homeroom = None
                    for h in homeroom_teachers:
                        if h["first_name"] == first_name and h["last_name"] == last_name:
                            found_homeroom = h
                            break

                    if found_homeroom is None:
                        print("Homeroom teacher '{} {}' not found.".format(
                            first_name, last_name))
                        continue

                    hr_class = found_homeroom["class_name"]

                    found_students = []
                    for s in students:
                        if s["class_name"] == hr_class:
                            found_students.append(s)

                    print("*" * 40)
                    print("Homeroom teacher: {} {}".format(first_name, last_name))
                    print("Leads class: {}".format(hr_class))
                    print("*" * 40)

                    if found_students:
                        print("Students:")
                        for s in found_students:
                            print("  - {} {}".format(s["first_name"], s["last_name"]))
                    else:
                        print("Students: (none in this class yet)")
                    print("*" * 40)

            # -- End (back to main menu) --
            elif manage_command == "end":
                break

    # ---- END ----
    elif command == "end":
        print("Goodbye!")
        break

