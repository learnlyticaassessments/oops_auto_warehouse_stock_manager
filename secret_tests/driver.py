import importlib.util
import datetime
import os
import random

def test_student_code(solution_path):
    report_dir = os.path.join(os.path.dirname(__file__), "..", "student_workspace")
    report_path = os.path.join(report_dir, "report.txt")
    os.makedirs(report_dir, exist_ok=True)

    spec = importlib.util.spec_from_file_location("student_module", solution_path)
    student_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(student_module)
    Analyzer = student_module.WarehouseStockManager

    report_lines = [f"=== Warehouse Manager Test at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ==="]

    randomized_failures = set()

    # 🧠 Anti-cheat randomized logic
    try:
        rand = Analyzer()
        rand.stock = {
            "USB": random.randint(10, 50),
            "SSD": random.randint(10, 20),
            "Cables": "Out of Stock"
        }

        rand.register_item("Mouse", 25)
        if rand.stock.get("Mouse", 0) != 25:
            randomized_failures.add("register_item")

        rand.stock = {"A": 10, "B": 3}
        rand.process_shipment({"A": 5, "B": 5})
        if rand.stock["A"] != 5 or rand.stock["B"] != "Out of Stock":
            randomized_failures.add("process_shipment")

        rand.stock = {"A": 10, "B": "Out of Stock", "C": "Out of Stock"}
        rand.restock_items(99)
        if rand.stock["B"] != 99 or rand.stock["C"] != 99:
            randomized_failures.add("restock_items")

        rand.stock = {"HDD": 5, "GPU": 30, "Fan": 8}
        report = rand.generate_low_stock_report(10)
        if report != {"HDD": 5, "Fan": 8}:
            randomized_failures.add("generate_low_stock_report")

    except Exception:
        randomized_failures.update([
            "register_item",
            "process_shipment",
            "restock_items",
            "generate_low_stock_report"
        ])

    # 🧪 Visible and Hidden test cases
    test_cases = [
        ("Visible", "Register Laptops 50", "register_item", ("Laptops", 50), {"Laptops": 50}),
        ("Visible", "Ship items", "process_shipment", ({"Laptops": 10, "Keyboards": 25},), {"Laptops": 40, "Keyboards": "Out of Stock"}),
        ("Visible", "Restock Out of Stock", "restock_items", (50,), {"Keyboards": 50}),
        ("Hidden", "Generate Low Stock Report", "generate_low_stock_report", (20,), {"Keyboards": 10, "Monitors": 5}),
        ("Hidden", "Multiple Items Out of Stock", "process_shipment", ({"Laptops": 50, "Keyboards": 15},), {"Laptops": "Out of Stock", "Keyboards": "Out of Stock"})
    ]

    for i, (section, desc, func, args, expected) in enumerate(test_cases, 1):
        try:
            analyzer = Analyzer()

            # 🛠️ Setup different stock for each function
            if func == "register_item":
                analyzer.stock = {}
            elif func == "restock_items":
                analyzer.stock = {"Laptops": 40, "Keyboards": "Out of Stock", "Monitors": 5}
            else:
                analyzer.stock = {"Laptops": 50, "Keyboards": 10, "Monitors": 5}

            method = getattr(analyzer, func)
            result = method(*args)

            # Anti-cheat check
            if func in randomized_failures:
                msg = f"❌ {section} Test Case {i} Failed due to randomized logic failure for {func}"
            else:
                if isinstance(result, dict) and isinstance(expected, dict):
                    filtered_result = {k: result.get(k) for k in expected}
                    passed = filtered_result == expected
                else:
                    passed = result == expected

                if passed:
                    msg = f"✅ {section} Test Case {i} Passed: {desc}"
                else:
                    msg = f"❌ {section} Test Case {i} Failed: {desc} | Expected={expected}, Got={filtered_result if 'filtered_result' in locals() else result}"

        except Exception as e:
            msg = f"❌ {section} Test Case {i} Crashed: {desc} | Error: {str(e)}"

        print(msg)
        report_lines.append(msg)

    # Save report
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines) + "\n")


