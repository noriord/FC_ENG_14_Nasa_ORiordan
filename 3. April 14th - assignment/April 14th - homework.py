print("Enter the maximum number of items to be shipped:")
max_items = int(input())

max_weight = 20
current_package_weight = 0  # accumulate item weights
packages_sent = 0  # count packages
total_weight_shipped = 0  # accumulate total weight
items_processed = 0  # count items processed
unused_capacities = []  # empty list to store unused capacities

while items_processed < max_items:
    print(f"Enter the weight of item {items_processed + 1} (kg) - between 1 to 10kg :")
    weight = int(input())

    # Handle termination
    if weight == 0:
        print("Weight of 0 entered. Terminating.")
        # Send current package if it has items
        if current_package_weight > 0:
            packages_sent += 1
            total_weight_shipped += current_package_weight
            unused_capacity = max_weight - current_package_weight
            unused_capacities.append(unused_capacity)
            print(f"Package {packages_sent} sent with weight {current_package_weight} kg")
        break

    # Validate weight range
    if weight < 1 or weight > 10:
        print("Weight must be between 1 to 10. Please try again.")
        continue

    # Check if adding this item exceeds package limit
    if current_package_weight + weight > max_weight:
        # Send current package
        packages_sent += 1
        total_weight_shipped += current_package_weight
        unused_capacity = max_weight - current_package_weight
        unused_capacities.append(unused_capacity)
        print(f"Package {packages_sent} sent with weight {current_package_weight} kg")

        # Start new package with current item
        current_package_weight = weight
    else:
        # Add item to current package
        current_package_weight += weight

    items_processed += 1

# Send final package if it has items
if current_package_weight > 0:
    packages_sent += 1
    total_weight_shipped += current_package_weight
    unused_capacity = max_weight - current_package_weight
    unused_capacities.append(unused_capacity)
    print(f"Package {packages_sent} sent with weight {current_package_weight} kg")

    # Display final statistics
    print("=" * 50)
    print("SHIPPING SUMMARY")
    print("=" * 50)
    print(f"Number of packages sent: {packages_sent}")
    print(f"Total weight of packages sent: {total_weight_shipped} kg")

    if packages_sent > 0:
        total_unused = (packages_sent * max_weight) - total_weight_shipped
    print(f"Total unused capacity: {total_unused} kg")

    # Find package with most unused capacity
    max_unused = max(unused_capacities)
    worst_package = unused_capacities.index(max_unused) + 1
    print(f"Package with most unused capacity: Package {worst_package} with {max_unused} kg unused")
else:
    print("No packages were sent.")
