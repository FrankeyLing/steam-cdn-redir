import listen
from edit_hosts import edit_hosts_file,restore_hosts_file


def get_cdn_use():
    file_path = 'cdn_use.txt'
    domain = None

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#') and line:
                domain = line
                break
    
    if domain:
        print("使用CDN:", domain)
    else:
        raise ValueError("无已启用的，请检查运行目录下cdn_use.txt")
        exit(1)
    return domain


def main():
    debug=False
    hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'
    backup_file_path = r'C:\Windows\System32\drivers\etc\hosts_backup'
    # backup_file_path = r"hosts_backup"
    # hosts_file_path = r"hosts"
    cdn_domain=get_cdn_use()
    edit_hosts_file(
        domain_to_comment=cdn_domain,
        backup_file_path=backup_file_path,
        hosts_file_path=hosts_file_path,
    )
    listen.cdn_domain=cdn_domain
    listen.run(r'ca.crt', r'ca.key','1234',debug)
    try:
        input('按Enter退出并恢复hosts文件')
    finally:
        restore_hosts_file(hosts_file_path, backup_file_path)

if __name__ == "__main__":
    main()

