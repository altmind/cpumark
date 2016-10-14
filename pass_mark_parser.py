# coding:utf-8
import urllib2
import re

pattern_rows = re.compile(r'(?m)<tr[^>]*>(.*?)</tr>\s*<tr class="tablesorter-childRow">(.*?)</tr>')
pattern_common_cols = re.compile(r'<td[^>]*?>(.*?)</td>')
pattern_common_col_link = re.compile(r'href="[^">]*id=([^">]*)">(.*?)</a>')
pattern_ext_cols = re.compile(
    r'(<span class="bold">([^<]+)</span>: (.*?)</div>)')  # outer () are unnecessary, remove and adjust indexes
pattern_link_text = re.compile(r'(<a[^>]*>(.*?)</a>|(.*))')

pattern_number = re.compile(r'[^0-9\.\-]+')


class PassMarkParser:
    def _strip_link(self, text):
        groups = pattern_link_text.search(text).groups()
        return groups[1] or groups[2]

    def _null_if_na(self, text):
        ts = text.strip()
        if ts == '' or ts == "NA" or ts == "Not Available" or ts is None:
            return None
        else:
            return text

    def _strip_not_numbers(self, text):
        return pattern_number.sub('', text)

    def _prepare_db_row(self, col_id, col_name, cols, ext_info):
        # Our text is already in utf8, just mark it unicode
        def u(text):
            if text is None:
                return None
            return text.decode('utf-8')

        response = {
            "id": int(col_id),
            "name": u(self._null_if_na(col_name)),
            "kind": u"cpu",
            "other_names": [],
            "price": self._null_if_na(self._strip_not_numbers(self._strip_link(cols[1]))),
            "cpu_mark": self._null_if_na(cols[2]),
            "cpu_value": self._null_if_na(self._strip_link(cols[3])),
            "cpu_st_mark": self._null_if_na(cols[4]),
            "cpu_st_value": self._null_if_na(cols[5]),
            "tdp": self._null_if_na(cols[6]),
            "power_perf": self._null_if_na(cols[7]),
            "test_date": u(self._null_if_na(cols[8])),
            "cpu_socket": u(self._null_if_na(cols[9])),
            "cpu_category": u(self._null_if_na(cols[10])),
            "ext": {}
        }
        for (_, column_name, column_value) in re.findall(pattern_ext_cols, ext_info):
            response["ext"][u(column_name.strip())] = self._null_if_na(u(column_value.strip()))
        return response

    def fetch_index_page(self):
        return urllib2.urlopen('https://www.cpubenchmark.net/CPU_mega_page.html').read()

    def parse_index_page(self, content):
        returned = []
        for (common_info, ext_info) in re.findall(pattern_rows, content):
            cols = re.findall(pattern_common_cols, common_info)
            # ext_cols = re.findall(pattern_common_cols, ext_info)
            # cols = map(lambda x: x[0], cols)
            (col_id, col_name) = pattern_common_col_link.search(cols[0]).groups()
            response = self._prepare_db_row(col_id, col_name, cols, ext_info)
            returned.append(response)
        return returned

    def fetch_and_parse(self):
        return self.parse_index_page(self.fetch_index_page())
