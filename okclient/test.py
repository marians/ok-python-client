# encoding: utf-8

import okclient
import unittest
from datetime import datetime


def suite():
    suite = unittest.TestSuite()
    suite.addTest(DocumentsTestCase("testDefaultSize"))
    return suite


class StreetsTestCase(unittest.TestCase):

    def setUp(self):
        self.oc = okclient.Client()

    def testSimple(self):
        streets = self.oc.streets(lat=50.959, lon=6.946)
        self.assertEqual(str(type(streets)),
            "<class 'okclient.StreetsResponse'>")
        self.assertTrue(streets.okay())
        self.assertTrue(len(streets) > 0)

    def testSmallRadius(self):
        """
        This request should only return one street
        (Matthias-Brüggen-Straße)
        """
        streets = self.oc.streets(lat=50.975347, lon=6.890944, radius=100)
        self.assertEqual(str(type(streets)),
            "<class 'okclient.StreetsResponse'>")
        self.assertTrue(streets.okay())
        self.assertTrue(len(streets) == 1)
        self.assertEqual(streets[0][0], u'Mathias-Br\xfcggen-Stra\xdfe')
        self.assertTrue(type(streets[0][1]), int)


class DocumentsTestCase(unittest.TestCase):

    def setUp(self):
        self.oc = okclient.Client()

    def testRequestSingle(self):
        response = self.oc.documents("AN/0105/2013")
        # test some general assumptions on all docs
        self.assertEqual(str(type(response)),
            "<class 'okclient.DocumentsResponse'>")
        self.assertTrue(response.okay())
        self.assertEqual(len(response), 1)
        self.assertEqual(response[0].date, datetime(2013, 1, 21))
        self.assertEqual(type(response[0].title), unicode)
        self.assertEqual(type(response[0].original_url), list)

    def testRequestSingleDefaultParam(self):
        response1 = self.oc.documents("AN/0105/2013")
        response2 = self.oc.documents(reference="AN/0105/2013")
        self.assertTrue(response1.okay())
        self.assertTrue(response2.okay())
        self.assertEqual(response1, response2)

    def testRequestSingleAttachments(self):
        response = self.oc.documents("3384/2008", attachments=True)
        self.assertTrue(response.okay())
        self.assertGreater(len(response[0].attachments), 0)

    def testRequestSingleThumbnails(self):
        response = self.oc.documents("3384/2008", thumbnails=True)
        self.assertTrue(response.okay())
        self.assertGreater(len(response[0].attachments[0].thumbnails), 0)
        self.assertTrue(str(type(response[0].attachments[0].thumbnails[0])),
            "<class 'okclient.Thumbnail'>")
        self.assertTrue(type(response[0].attachments[0].thumbnails[0].page),
            int)

    def testRequestSingleConsultations(self):
        response = self.oc.documents("3384/2008", consultations=True)
        self.assertTrue(response.okay())
        self.assertGreater(len(response[0].consultations), 0)

    def testSearch(self):
        response = self.oc.documents(query="stadtbahn")
        self.assertTrue(response.okay())
        self.assertGreater(len(response), 0)


class LocationsTestCase(unittest.TestCase):

    def setUp(self):
        self.oc = okclient.Client()

    def testSimple(self):
        response = self.oc.locations("Gertrudenstraße")
        self.assertEqual(str(type(response)),
            "<class 'okclient.LocationsResponse'>")
        self.assertTrue(response.okay())
        self.assertTrue(response.nodes is not None)
        self.assertTrue(response.averages is not None)
        self.assertTrue(len(response.nodes) > 0)
        self.assertTrue(len(response.averages[0]) == 2)

    def testUnknownStreet(self):
        response = self.oc.locations("Gertrudenstr")
        self.assertEqual(str(type(response)),
            "<class 'okclient.LocationsResponse'>")
        self.assertFalse(response.okay())

    def testWithoutNodes(self):
        response = self.oc.locations("Alpenerstraße", nodes=False)
        self.assertEqual(str(type(response)),
            "<class 'okclient.LocationsResponse'>")
        self.assertTrue(response.okay())
        self.assertTrue(response.nodes is None)
        self.assertTrue(response.averages is not None)

    def testWithoutAverages(self):
        response = self.oc.locations("Venloer Straße", averages=False)
        self.assertEqual(str(type(response)),
            "<class 'okclient.LocationsResponse'>")
        self.assertTrue(response.okay())
        self.assertTrue(response.averages is None)
        self.assertTrue(response.nodes is not None)


if __name__ == '__main__':
    unittest.main()
