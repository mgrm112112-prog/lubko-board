import sys
import json
import argparse
import urllib.request
import urllib.error

def list_boards(api_url):
    """عرض لوحات المشكلات المتاحة"""
    print(f"[*] جاري الاتصال بـ Lubko API لجلب اللوحات...")
    try:
        req = urllib.request.Request(f"{api_url}/boards", headers={'User-Agent': 'Lubko-CLI-Client/1.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("\n[+] اللوحات المتاحة (Issue Boards):")
            for board in data:
                print(- ID: {board.get('id')} | Name: {board.get('name')})
    except Exception as e:
        print(f"[-] تعذر جلب اللوحات: {str(e)}")

def create_issue(api_url, board_id, title, description):
    """إنشاء مشكلة جديدة في اللوحة"""
    print(f"[*] جاري إنشاء مشكلة جديدة في اللوحة ID: {board_id}...")
    payload = json.dumps({"title": title, "description": description, "board_id": board_id}).encode('utf-8')
    try:
        req = urllib.request.Request(f"{api_url}/issues", data=payload, headers={'Content-Type': 'application/json', 'User-Agent': 'Lubko-CLI-Client/1.0'})
        with urllib.request.urlopen(req) as response:
            print("[+] تم إنشاء المشكلة وإضافتها للوحة بنجاح!")
    except Exception as e:
        print(f"[-] خطأ أثناء إنشاء المشكلة: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lubko Board CLI Management Tool")
    parser.add_argument("--url", default="http://localhost:8080/api", help="Lubko API Base URL")
    subparsers = parser.add_subparsers(dest="command")

    # أمر عرض اللوحات
    subparsers.add_parser("boards", help="عرض جميع اللوحات المتاحة")

    # أمر إنشاء تذكرة/مشكلة جديدة
    issue_parser = subparsers.add_parser("create-issue", help="إنشاء مشكلة جديدة في لوحة معينة")
    issue_parser.add_argument("--board", required=True, help="معرف اللوحة (Board ID)")
    issue_parser.add_argument("--title", required=True, help="عنوان المشكلة")
    issue_parser.add_argument("--desc", default="", help="وصف تفصيلي للمشكلة")

    args = parser.parse_args()

    if args.command == "boards":
        list_boards(args.url)
    elif args.command == "create-issue":
        create_issue(args.url, args.board, args.title, args.desc)
    else:
        parser.print_help()