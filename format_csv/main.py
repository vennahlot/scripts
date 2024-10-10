import argparse
import csv

parser = argparse.ArgumentParser(description="Extract standard from content")
parser.add_argument("csv_file", type=str, help="CSV file to extract standard from")
args = parser.parse_args()


def extract_std_from_content(content: str) -> list[list[str]]:
    new_rows = []  # std_num, std, sub_std_num, sub_std
    std_idx = ""
    std_name = ""
    for line in content.split("\n"):
        if "." not in line:
            continue
        idx, text = line.strip().split(".", 1)
        if idx.isdigit():
            std_idx = idx.strip()
            std_name = text.strip()
        elif std_idx and std_name:
            new_rows.append([std_idx, std_name, idx.strip(), text.strip()])
    if std_idx and std_name and not new_rows:
        new_rows.append([std_idx, std_name, "", ""])
    return new_rows


def main():
    grade_rows_mapping: dict[str, list[list[str]]] = {}
    with open(args.csv_file) as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        for i, row in enumerate(reader):
            if i == 0:
                continue
            theme = row[0]
            if not theme:
                continue
            for i in range(1, 7):
                grade = str(i - 1) if i != 1 else "k"
                new_rows = extract_std_from_content(row[i])
                if grade not in grade_rows_mapping:
                    grade_rows_mapping[grade] = []
                for new_row in new_rows:
                    grade_rows_mapping[grade].append([theme] + new_row)

    out_fname = "format_" + args.csv_file.split("/")[-1]
    out_fpath = args.csv_file.replace(args.csv_file.split("/")[-1], out_fname)
    with open(out_fpath, "w", encoding="utf-8") as f:
        csv_writer = csv.writer(f, delimiter=",", quotechar='"')
        csv_writer.writerow(["grade", "theme", "std_num", "std", "sub_std_num", "sub_std"])
        for grade, rows in grade_rows_mapping.items():
            for row in rows:
                csv_writer.writerow([grade] + row)


if __name__ == "__main__":
    main()
