# encoding: utf-8

import okclient
import unittest
from datetime import datetime


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DocumentsTestCase("testDefaultSize"))
    return suite


class DocumentsTestCase(unittest.TestCase):

    def setUp(self):
        self.oc = okclient.Client()

    def testRequestSingle(self):
        response = self.oc.documents("AN/0105/2013")
        # test some general assumptions on all docs
        self.assertEqual(str(type(response)),
            "<class 'okclient.DocumentsResponse'>")
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].date, datetime(2013, 1, 21))
        self.assertEqual(type(response[0].title), unicode)
        self.assertEqual(type(response[0].original_url), list)

    def testRequestSingleDefaultParam(self):
        response1 = self.oc.documents("AN/0105/2013")
        response2 = self.oc.documents(reference="AN/0105/2013")
        self.assertEqual(response1, response2)

    def testRequestSingleAttachments(self):
        response = self.oc.documents("3384/2008", attachments=True)
        self.assertGreater(len(response[0].attachments), 0)

    def testRequestSingleThumbnails(self):
        response = self.oc.documents("3384/2008", thumbnails=True)
        self.assertGreater(len(response[0].attachments[0].thumbnails), 0)
        self.assertTrue(str(type(response[0].attachments[0].thumbnails[0])),
            "<class 'okclient.Thumbnail'>")
        self.assertTrue(type(response[0].attachments[0].thumbnails[0].page),
            int)

    def testRequestSingleConsultations(self):
        response = self.oc.documents("3384/2008", consultations=True)
        self.assertGreater(len(response[0].consultations), 0)

    def testSearch(self):
        response = self.oc.documents(query="stadtbahn")
        self.assertGreater(len(response), 0)



if __name__ == '__main__':
    unittest.main()
