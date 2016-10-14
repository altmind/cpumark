import urllib2
import re

pattern_rows = re.compile(r'(?m)<tr[^>]*>(.*?)</tr>\s*<tr class="tablesorter-childRow">(.*?)</tr>')
pattern_common_cols = re.compile(r'<td[^>]*?>(.*?)</td>')
pattern_common_col_link = re.compile(r'href="[^">]*id=([^">]*)">(.*?)</a>')
pattern_ext_cols = re.compile(r'(<span class="bold">([^<]+)</span>: (.*?)</div>)')

pattern_link_text = re.compile(r'(<a[^>]*>(.*?)</a>|(.*))')


class PassMarkParser:
    def _strip_link(self, text):
        groups = pattern_link_text.search(text).groups()
        return groups[1] or groups[2]

    def fetch_index_page(self):
        return urllib2.urlopen('https://www.cpubenchmark.net/CPU_mega_page.html').read()

    def fetch_and_parse(self):
        content = self.fetch_index_page()
        returned = []
        for (common_info, ext_info) in re.findall(pattern_rows, content):
            cols = re.findall(pattern_common_cols, common_info)
            # ext_cols = re.findall(pattern_common_cols, ext_info)
            # cols = map(lambda x: x[0], cols)
            (col_id, col_name) = pattern_common_col_link.search(cols[0]).groups()
            response = {
                "id": col_id,
                "name": col_name,
                "price": self._strip_link(cols[1]),
                "cpu_mark": cols[2],
                "cpu_value": self._strip_link(cols[3]),
                "single_thread_mark": cols[4],
                "single_thread_value": cols[5],
                "tdp": cols[6],
                "power_perf": cols[7],
                "test_date": cols[8],
                "socket": cols[9],
                "category": cols[10],
                "ext": {}
            }
            for (_, column_name, column_value) in re.findall(pattern_ext_cols, ext_info):
                response["ext"][column_name.strip()] = column_value.strip()
            returned.append(response)
        return returned
