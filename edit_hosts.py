import shutil


def read_hosts_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return lines


def backup_hosts_file(file_path, backup_path):
    shutil.copyfile(file_path, backup_path)


def restore_hosts_file(file_path, backup_path):
    shutil.copyfile(backup_path, file_path)


def append_to_hosts_file(file_path, text):
    with open(file_path, "a") as file:
        file.write(text)


def comment_out_domain(domain, content):
    lines = content.split("\n")
    modified_lines = []
    for line in lines:
        if domain in line:
            modified_lines.append("# " + line)
        else:
            modified_lines.append(line)
    return "\n".join(modified_lines)


def edit_hosts_file(
    domain_to_comment=None,
    debugMode=True,
    backup_file_path=r"hosts_backup",
    hosts_file_path=r"hosts",
):

    # 备份hosts文件
    backup_hosts_file(hosts_file_path, backup_file_path)

    # # 读取hosts文件
    # hosts_content = read_hosts_file(hosts_file_path)

    # # 打印读取的内容
    # for line in hosts_content:
    #     print(line.strip())

    # 定义locales集合和结果列表
    locales = {
        "lax",
        "iad",
        "fra",
        "atl",
        "sto",
        "hkg",
        "gru",
        "ord",
        "man",
        "sea",
        "lhr",
        "tyo",
        "mad",
        "par",
        "syd",
        "scl",
        "ams",
        "waw",
        "sgp",
        "vie",
        "sto",
        "jnb",
        "seo",
    }

    result = []
    for i in range(31):
        for locale in locales:
            for j in range(41):
                result.append(f"127.0.0.1 cache{i}-{locale}{j}.steamcontent.com")

    # 将结果连接成一个字符串，每个字符串一行
    result_str = "\n".join(result)

    # 在result_str前面添加指定的条目
    others_international_domain_str = """127.0.0.1 google.cdn.steampipe.steamcontent.com
127.0.0.1 google2.cdn.steampipe.steamcontent.com
127.0.0.1 edge.steam-dns.top.comcast.net
127.0.0.1 steam.eca.qtlglb.com
127.0.0.1 steam.naeu.qtlglb.com
127.0.0.1 steam.ru.qtlglb.com
127.0.0.1 steampipe-kr.akamaized.net
127.0.0.1 steampipe-partner.akamaized.net
127.0.0.1 steampipe.akamaized.net
127.0.0.1 f3b7q2p3.ssl.hwcdn.net
127.0.0.1 telus.cdn.steampipe.steamcontent.com
127.0.0.1 steam.cdn.on.net
127.0.0.1 steam.cdn.orcon.net.nz
127.0.0.1 steam.cdn.slingshot.co.nz
127.0.0.1 steam.cdn.webra.ru
127.0.0.1 alibaba.cdn.steampipe.steamcontent.com
"""


    internal_domain = """
127.0.0.1 cdn-ws.content.steamchina.com
127.0.0.1 cdn.mileweb.cs.steampowered.com.8686c.com
127.0.0.1 dl.steam.clngaa.com
127.0.0.1 steampipe.steamcontent.tnkjmec.com
127.0.0.1 cdn-qc.content.steamchina.com
127.0.0.1 cdn-ali.content.steamchina.com
127.0.0.1 xz.pphimalayanrt.com
127.0.0.1 st.dl.eccdnx.com
127.0.0.1 st.dl.bscstorage.net
"""

    internal_domain = comment_out_domain( domain_to_comment,internal_domain)

    # 合并前缀和结果字符串
    full_str = internal_domain + others_international_domain_str + result_str

    append_to_hosts_file(hosts_file_path, full_str + "\n")




if __name__ == "__main__":
    # 定义hosts文件路径
    # hosts_file_path = r'C:\Windows\System32\drivers\etc\hosts'
    # backup_file_path = r'C:\Windows\System32\drivers\etc\hosts_backup'
    backup_file_path = r"hosts_backup"
    hosts_file_path = r"hosts"
    edit_hosts_file(
        domain_to_comment="dl.steam.clngaa.com",
        backup_file_path=backup_file_path,
        hosts_file_path=hosts_file_path,
    )
    # restore_hosts_file(hosts_file_path, backup_file_path)
