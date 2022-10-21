#!/usr/bin/python3
import json
import os
import requests
from SSPICUtils import icreportutils
import xml.etree.ElementTree as ET
import logging
from internal.dbutils import DbUtils
from apps import AppConfig

class ictriageutils(object):
    def __init__(self,build_label,service,report_id):
        self.build_label = build_label
        self.service = service
        self.icutils = icreportutils(build_label,service,report_id)
        self.test_run_id = None

    def get_junit_data(self,junit_url):
        resp = self.icutils.get_response(junit_url)
        report_file = os.path.join(self.build_label + "_" + self.service, "junit_report.xml")

        if not resp :
            return None

        with open(report_file, 'wb') as f:
            f.write(resp.content)
        return report_file

    def get_ic_report(self):
        # Create Local unique directory
        os.makedirs(self.icutils.build_label + "_" + self.icutils.service, exist_ok=True)

        urls = self.icutils.get_all_urls()
        katalon_urls = self.get_katalon_collection_urls(urls)
        logging.debug("Katalon urls", katalon_urls)

        tcd = dict()
        '''for component in self.icutils.components:
            tcd[component]=[]
            for comp_colls in urls[component]:
                data = self.icutils.get_katalon_component_report(urls[component][comp_colls])
                #print(comp_colls, urls[component][comp_colls])
                if data:
                    json_data = data.json()
                    if 'TestCaseSummary' in json_data.keys():
                        for test_case in json_data['TestCaseSummary']:
                            tcd[component].append(test_case)
        self.icutils.write_katalon_test_cases(tcd)'''
        for report_url in katalon_urls:
            self.get_all_katalon_test_cases(report_url,tcd)

        self.icutils.write_katalon_test_cases(tcd)

        #Get Junit data
        if 'junit' not in urls.keys():
            logging.debug("No junit report foung")
            return
        junit_xml_file = self. get_junit_data(urls['junit'])
        junit_test_cases = []
        tree = ET.parse(junit_xml_file)
        root = tree.getroot()

        for item in root :
            if item.tag == 'Component':
                #component_tcd = dict()
                for Execution in item:
                    for Suites in Execution:
                        if Suites.tag == 'Suite':
                            for Suite in Suites:
                                tc = dict()

                                for case in Suite:
                                    if case.tag == "Case":

                                        tc['Component'] = item.attrib['Name']
                                        tc['Area'] = item.attrib['FunctionalArea']
                                        tc['Suites'] = Suites.attrib['Name']
                                        tc['Name'] = case.attrib['Id']
                                        tc['Status']=case.attrib['Status']
                                        tc['StartTime'] = case.attrib['StartTime']
                                        tc['ExecTime'] = case.attrib['ElapsedTime']

                                        for case_data in case:
                                            if case_data.tag == "AdditionalInfo" :
                                                for case_data_item in case_data:
                                                    if case_data_item.attrib['Name'] == "Realm" :
                                                        tc['Realm'] = case_data_item.text
                                                    if case_data_item.attrib['Name'] == "NodeId" :
                                                        tc['NodeId'] = case_data_item.text

                                            if case_data.tag == "Message":
                                                #tc['Message'] = case_data.text
                                                pass
                                            #print(case_data.tag)

                                junit_test_cases.append(tc)

        self.icutils.write_junit_test_cases(junit_test_cases)
        return

    def get_katalon_collection_urls(self, urls):

        katalon_urls = []
        for components in urls.keys():
            if components == 'junit':
                continue
            for coll_url in urls[components]:
                summary_url = urls[components][coll_url]
                test_run_url = summary_url.split('/Summary-Report.json')[0]
                print(test_run_url)

                # get the test Run ID for unique identifications

                if not self.test_run_id :
                    for item in test_run_url.split('/'):
                        if 'katalon_' in item :
                            self.test_run_id = item.split('katalon_')[1]

                if test_run_url :
                    report_url = self.get_xml_url(test_run_url)
                    if report_url :
                        katalon_urls.append(report_url)
        return katalon_urls

    def get_all_katalon_test_cases(self,report_url,tcs):
        #tcs = dict()

        if report_url :
            xml_data = requests.get(report_url)
            report_tree = ET.fromstring(xml_data.text)
            root = report_tree
            if root.tag == "testsuites":
                self. get_all_katalon_test_cases_from_xml(root,tcs)
        return tcs

    def get_all_katalon_test_cases_from_xml(self,root,tcs):
        #tcd = dict()
        for testsuite in root:

            for testcase in testsuite:
                if testcase.tag =='testcase':
                    tc = dict()
                    tc['Suites'] = testsuite.attrib['name']
                    tc['Name'] = testcase.attrib['name']
                    tc['Status'] = testcase.attrib['status']
                    tc['ExecTime'] =testcase.attrib['time']
                    tc['test_run_id'] = self.test_run_id
                    tc['StartTime'],tc['EndTime'],tc['Realm'] = self.get_realm_data(testcase)
                    tcs[testcase.attrib['name']] = tc

        return tcs

    def get_realm_data(self,tc):
        test_start_time = None
        test_end_time = None
        realm = None
       # print("==================================")
        for child in tc:
            if child.tag == "system-out":
                line = ""
                # Get the test start time
                lines = child.text.split('\n')
                #print(lines)

                test_start_time = lines[0].split(' - ')[0]
                test_end_time = lines[-1].split(' - ')[0]

                # Get
                for line in child.text.split('\n'):
                    if "[MESSAGE][INFO]" in line and "ReceiveAssignedRealm:" in line:
                        realm = line.split('ReceiveAssignedRealm:')[-1]
                        logging.debug("realm found",realm)
                        break
       # print("==================================")
        return test_start_time,test_end_time,realm

    def get_xml_url(self, comp_url):
        #print(comp_url)
        resp = self.icutils.get_response(comp_url)
        t_data = self.icutils.get_all_hrefs(resp)
        collection = comp_url.split('/')[-1]
        for item in t_data :
            if '_' in item.text and '/' in item.text :
                comp_url = comp_url + '/' + item.text + collection + '-Custom/'
                resp = self.icutils.get_response(comp_url)
                href_data = self.icutils.get_all_hrefs(resp)
                if href_data :
                    for item in href_data:
                        if '_' in item.text:
                            return comp_url + item.text + 'JUnit_Report.xml'
                else :
                    return comp_url

    def generate_katalon_csv(self):
        # NOT USED , this is for future development for analytics
        filepath = self.build_label+'_'+self.service
        filename = os.path.join(filepath,'katalon.json')
        if not os.path.exists(filename):
            self.get_ic_report()
        csv_filename = os.path.join(filepath,"katalon.csv")

        with open(filename,'r') as katalon_file:
            katalon_test_cases = json.load(katalon_file)
            #print(katalon_test_cases)
            for test_case in katalon_test_cases.keys():
                pass

    def insert_katalon_data(self):

        filepath = self.build_label + '_' + self.service
        filename = os.path.join(os.getcwd(),filepath, 'katalon.json')
        with open(filename,'r') as fp :
            data = json.load(fp)
            db_obj = DbUtils(AppConfig.username,AppConfig.password,AppConfig.dbhost,AppConfig.dbport,AppConfig.dbname)
            db_obj.get_connection()
            # insert katalon test data
            sql_query = self.prepare_insert_query_for_tables("SSP_IC_KATALON_TEST_DATA",data)
            for item in data :
                sql_data = (data[item]['test_run_id'],"",data[item]['Suites'],data[item]['Name'],data[item]['Status'],data[item]['StartTime'],data[item]['EndTime'],data[item]['ExecTime'],data[item]['Realm'],"",self.service,self.build_label)
                db_obj.insert_data(sql_query,sql_data)
            db_obj.close_connection()
            return

    def prepare_insert_query_for_tables (self,table_name, data):
        sql_query = ''
        if table_name == "SSP_IC_KATALON_TEST_DATA" :
            sql_query = "insert into \"" + table_name + "\"( \"test_run_id\",\"Component\",\"Suites\",\"Name\",\"Status\",\"StartTime\",\"EndTime\",\"ExecTime\",\"Realm\",\"NodeId\",\"service\",\"build_label\") values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        #print(sql_query)
        return sql_query

def get_report_metdata(report_url):
    url_data = report_url.split('/')
    service = url_data[3]
    build_lable = url_data[10]
    report_id = '_'.join(url_data[11].split('_')[2:4])
    return  service, build_lable, report_id


def main():
    report_url = "http://gcpperf01-exportfs-z3-0.lab-us.gcpint.ariba.com:8080/gcpic01/gcp/katalon/buyer/gcpic01/IC/consolidated/SSP.2022.gTrunk-10513/gcp_buyer_20221008_032333_email_report.html"
    service,build_label,report_id = get_report_metdata(report_url)
    print(build_label,service,report_id)
    os.makedirs(build_label+"_"+service, exist_ok=True)
    obj = ictriageutils(build_label, service,report_id)
    obj.get_ic_report()
    #obj.generate_katalon_csv()
    obj.insert_katalon_data()


if __name__ == "__main__":
    main()
