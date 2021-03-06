__author__ = 'shanesully'

import sys
from BeautifulSoup import BeautifulStoneSoup


def display_usage():
    print "\nUsage:\n\n\t$ python {} $OPTIONS $XML_FILES\n", \
          "\nOptions:\n", \
          "\t-c: Combine n strings.xml file(s) into a single xml language file\n", \
          "\t-e: Extract strings from a strings.xml file\n".format(sys.argv[0])


def extract_strings(files):
    for given_file in files:
        file_format = str(given_file).split('.')[1]

        if file_format == 'xml':
            with open(given_file) as xml_source_file:
                # New file name
                strings_file_name = str(xml_source_file.name).split('.')[0] + '_strings.txt'

                with open(strings_file_name, 'w+') as strings_file:
                    soup = BeautifulStoneSoup(xml_source_file)
                    strings = []

                    for tag in soup.findAll(['string', 'plurals']):
                       strings.append(tag.text.encode('utf-8'))

                    for string in strings:
                        strings_file.write(string + '\n')

                    print "Created {} containing {} strings".format(strings_file_name, len(strings))
        else:
            print "Ignoring {} as it is in .{} format and not .xml".format(given_file, str(given_file).split('.')[1])


def combine_files(files):
    '''Combine values from multiple files'''
    strings = {}

    for given_file in files:
        with open(given_file) as xml_source_file:
            soup = BeautifulStoneSoup(xml_source_file)

            for tag in soup.findAll(['string', 'plurals']):
                if str(tag['name']) in strings:
                    strings[str(tag['name'])].append(tag.text)
                else:
                    strings[str(tag['name'])] = [tag.text]

    with open('combined_strings.xml', 'w+') as combined_strings_file:
        xml_header = '<?xml version="1.0" encoding="UTF-8"?>\n<resources>'
        xml_footer = '</resources>'

        combined_strings_file.write('{}\n'.format(xml_header))

        for key, value_list in strings.iteritems():
            combined_strings_file.write("\t<key>{}</key>\n".format(key))

            for value in value_list:
                combined_strings_file.write("\t<string>{}</string>\n".format(value.encode('utf8')))
        
        combined_strings_file.write('{}\n'.format(xml_footer))

        print "\n{} file created\n".format(combined_strings_file.name)


def main():
    if sys.argv[1] == '-e':
        extract_strings(sys.argv[2:])
    elif sys.argv[1] == '-c':
        combine_files(sys.argv[2:])
    else:
       display_usage() 


if __name__ == '__main__':

    if len(sys.argv) <= 1:
        display_usage()
        sys.exit()

    main()

