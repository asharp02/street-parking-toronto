import os
import xml.etree.ElementTree as ET

from django.core.management import call_command
from django.test import TestCase, SimpleTestCase
from whereToPark.management.commands.get_parking_dump import (
    Command as GetParkingDumpCmd,
)
from whereToPark.management.commands.import_parking_data import (
    Command as ImportParkingCmd,
)
from whereToPark.management.commands.set_location_data import Command as SetParkingCmd

from whereToPark.models import NoParkingByLaw, RestrictedParkingByLaw

# Create your tests here.


def file_exists(directory, filename):
    root_path = os.getcwd()
    file_path = os.path.join(root_path, directory, filename)
    return os.path.exists(file_path)


class GetParkingDumpTests(SimpleTestCase):
    def test_fetch_data_folder_outputs_zipped_folder(self):
        GetParkingDumpCmd().fetch_data_folder()
        directory = ""
        filename = "parking_schedules.zip"
        self.assertTrue(file_exists(directory, filename))

    def test_unzip_files_in_right_folder(self):
        GetParkingDumpCmd().unzip_files()
        directory = "fixtures"
        no_parking_filename = "no_parking.xml"
        restricted_parking_filename = "restricted_parking.xml"
        self.assertTrue(file_exists(directory, no_parking_filename))
        self.assertTrue(file_exists(directory, restricted_parking_filename))


class SetLocationDataTests(TestCase):
    def setUp(self):
        NoParkingByLaw.objects.create(
            bylaw_no="[Repealed 2016-04-05 by By-law No. 365-2016]",
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            prohibited_times_and_or_days="12 hours",
            between_street_a="Glenholme Avenue",
            between_street_b="Oakwood Avenue",
        )
        RestrictedParkingByLaw.objects.create(
            bylaw_no="[Repealed 2016-04-05 by By-law No. 365-2016]",
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            times_and_or_days="12 hours",
            max_period_permitted="12 hours",
            between_street_a="Glenholme Avenue",
            between_street_b="Oakwood Avenue",
        )

    def test_simple_between_field_produces_correct_lat_lng(self):
        SetParkingCmd().handle_no_parking_locations()
        law = NoParkingByLaw.objects.get(id=1)
        self.assertAlmostEqual(law.boundary_a_lat, 43.689936, delta=0.00005)
        self.assertAlmostEqual(law.boundary_a_lng, -79.442908, delta=0.0005)
        self.assertAlmostEqual(law.boundary_b_lat, 43.690593, delta=0.00005)
        self.assertAlmostEqual(law.boundary_b_lng, -79.440109, delta=0.0005)

    def test_simple_between_field_produces_correct_lat_lng_restricted(self):
        SetParkingCmd().handle_restricted_locations()
        law = RestrictedParkingByLaw.objects.get(id=1)
        self.assertAlmostEqual(law.boundary_a_lat, 43.689936, delta=0.00005)
        self.assertAlmostEqual(law.boundary_a_lng, -79.442908, delta=0.0005)
        self.assertAlmostEqual(law.boundary_b_lat, 43.690593, delta=0.00005)
        self.assertAlmostEqual(law.boundary_b_lng, -79.440109, delta=0.0005)

    def test_simple_between_field_parsed(self):
        law = NoParkingByLaw.objects.get(id=1)
        street_a, street_b = SetParkingCmd().handle_between_field(law)
        self.assertEqual(street_a, "Glenholme Avenue")
        self.assertEqual(street_b, "Oakwood Avenue")

    def test_complex_between_field_doesnt_save_location(self):
        NoParkingByLaw.objects.create(
            bylaw_no="[Repealed 2016-04-05 by By-law No. 365-2016]",
            source_id="2",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway="Ashbury Avenue",
            side="North",
            between="Brock Avenue and the west end of Abbs Street",
            prohibited_times_and_or_days="12 hours",
        )
        SetParkingCmd().handle_no_parking_locations()
        law = NoParkingByLaw.objects.get(id=2)
        self.assertIsNone(law.boundary_a_lat)
        self.assertIsNone(law.boundary_a_lng)
        self.assertIsNone(law.boundary_b_lat)
        self.assertIsNone(law.boundary_b_lng)

    def test_parse_geocode_xml(self):
        sample_xml = "<geodata>\
                        <latt>43.690601</latt>\
                        <longt>-79.439944</longt>\
                        <city>toronto</city>\
                        <prov>ON</prov>\
                        <street1>ashbury avenue</street1>\
                        <street2>oakwood avenue</street2>\
                        <confidence>0.9</confidence>\
                    </geodata>"
        tree = ET.fromstring(sample_xml)
        lat, lng = SetParkingCmd().parse_geocode_xml(tree)
        self.assertEqual(lat, 43.690601)
        self.assertEqual(lng, -79.439944)


class ImportParkingDataTests(TestCase):
    def setUp(self):
        call_command("import_parking_data")
        np_tree = ET.parse("fixtures/no_parking.xml")
        self.np_root = np_tree.getroot()

        rp_tree = ET.parse("fixtures/restricted_parking.xml")
        self.rp_root = rp_tree.getroot()

    def test_between_street_a_and_b_fields_set_no_parking(self):
        law = NoParkingByLaw.objects.first()
        between = law.between
        self.assertEqual(law.between_street_a, between.split(" and ")[0])
        self.assertEqual(law.between_street_b, between.split(" and ")[1])

    def test_between_street_a_and_b_fields_set_restricted(self):
        law = RestrictedParkingByLaw.objects.first()
        between = law.between
        self.assertEqual(law.between_street_a, between.split(" and ")[0])
        self.assertEqual(law.between_street_b, between.split(" and ")[1])

    def test_noparkingbylaw_model_count_matches_xml_file(self):
        self.assertEqual(
            NoParkingByLaw.objects.count(), len(self.np_root.getchildren())
        )

    def test_restrictedparkingbylaw_model_count_matches_xml_file(self):
        self.assertEqual(
            RestrictedParkingByLaw.objects.count(), len(self.rp_root.getchildren())
        )

    def test_no_parking_cmd_does_not_create_duplicates(self):
        total_count_pre = NoParkingByLaw.objects.count()
        ImportParkingCmd().import_no_parking()

        self.assertEqual(total_count_pre, NoParkingByLaw.objects.count())

        first_id = NoParkingByLaw.objects.first().source_id
        count_with_id = NoParkingByLaw.objects.filter(source_id=first_id).count()
        self.assertEqual(count_with_id, 1)

    def test_restricted_parking_cmd_does_not_create_duplicates(self):
        total_count_pre = RestrictedParkingByLaw.objects.count()
        ImportParkingCmd().import_restricted_parking()
        self.assertEqual(total_count_pre, RestrictedParkingByLaw.objects.count())

        first_id = RestrictedParkingByLaw.objects.first().source_id
        count_with_id = RestrictedParkingByLaw.objects.filter(
            source_id=first_id
        ).count()
        self.assertEqual(count_with_id, 1)
