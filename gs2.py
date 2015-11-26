#!/usr/bin/env python3
import os
import json
import jmath


def load_json(filename, gs2_list=[]):
    del gs2_list[:]
    with open(filename, 'r') as json_file:
        data = json.load(json_file)
        for f in data:
            tmp_file = GS2File()
            tmp_file.name = f["name"]

            for sec in f["sections"]:
                tmp_section = GS2Section()
                tmp_section.name = sec["name"]
                for propName, propValue in sec["properties"].items():
                    tmp_section.properties[propName] = propValue
                tmp_file.sections.append(tmp_section)
            gs2_list.append(tmp_file)
    return gs2_list


def save_json(gs2_list, filename):
    with open(filename, "w") as json_file:
        json_file.write(str(gs2_list))


class GS2File(object):
    def __init__(self):
        self.name = None
        self.sections = []

    def __repr__(self):
        ret_str = "{\"name\":\"" + str(self.name) + "\", \"sections\":["
        for sect in self.sections[:-1]:
            ret_str += str(sect) + ","
        ret_str += str(self.sections[-1])
        ret_str += "]}"

        return ret_str

    def process_file(self, filename, maxlines=-1):
        f = open(filename, 'r', encoding="latin-1")  # Open the file so we can read it
        self.name = str(os.path.split(filename)[1].strip())  # Set name of object
        current_section = None
        current_line = 1
        max_line = 100
        for line in f:
            if current_line > max_line and maxlines is not -1:
                break

            # Skip blank lines
            if line.strip() == "":
                continue

            # Add section to file object
            if line.startswith("##"):
                if current_section is not None:
                    self.sections.append(current_section)

                current_section = GS2Section()
                current_section.name = str(line[2:].strip())  # Get Sectionname
            else:
                # Add property to section
                # print "name: '" + line[1:].split('=')[0].strip()+"', value: '"+ line[1:].split('=')[1].strip()+"'"
                current_section.properties[str(line[1:].split('=')[0].strip())] = str(
                    line[1:].split('=')[1].strip())
            current_line += 1
        f.close()


class GS2Section(object):
    def __init__(self):
        self.name = None
        self.properties = {}

    def get_values(self):
        if "Value" in self.properties:
            return [float(x) for x in self.properties["Value"].translate({ord(i): None for i in '<>'}).split()]

    def get_peak_threshold(self):
        return jmath.standard_deviation(self.get_values())


    def __repr__(self):
        return json.dumps(self.__dict__)
