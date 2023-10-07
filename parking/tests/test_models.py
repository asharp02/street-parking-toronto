from django.test import TestCase

from whereToPark.models import (
    NoParkingByLaw,
    RestrictedParkingByLaw,
    Highway,
    Intersection,
)


class ByLawModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        highway = Highway.objects.create(name="queen street", street_end="W")
        cross_street_1 = Highway.objects.create(name="dowling avenue", street_end="W")
        cross_street_2 = Highway.objects.create(name="jameson avenue", street_end="W")

        intersection_1 = Intersection.objects.create(
            main_street=highway,
            cross_street=cross_street_1,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )
        intersection_2 = Intersection.objects.create(
            main_street=highway,
            cross_street=cross_street_2,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )


class NoParkingByLawModelTest(ByLawModelTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # setup objects used by all test methods
        NoParkingByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=highway,
            boundary_start=intersection_1,
            boundary_end=intersection_2,
            side="North",
            between="Dowling Avenue and Jameson Avenue",
            prohibited_times_and_or_days="12 hours",
        )

    def test_source_id(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("source_id").verbose_name
        self.assertEqual(field_label, "source id")

    def test_schedule_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule").verbose_name
        self.assertEqual(field_label, "schedule")

    def test_schedule_name_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule_name").verbose_name
        self.assertEqual(field_label, "schedule name")

    def test_highway_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("highway").verbose_name
        self.assertEqual(field_label, "highway")

    def test_side_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("side").verbose_name
        self.assertEqual(field_label, "side")

    def test_between_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("between").verbose_name
        self.assertEqual(field_label, "between")

    def test_prohibited_times_and_or_days_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("prohibited_times_and_or_days").verbose_name
        self.assertEqual(field_label, "prohibited times and or days")

    def test_boundary_start_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_start").verbose_name
        self.assertEqual(field_label, "boundary start")

    def test_boundary_end_label(self):
        law = NoParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_end").verbose_name
        self.assertEqual(field_label, "boundary end")

    def test_str_method(self):
        law = NoParkingByLaw.objects.get(id=1)
        self.assertEqual(law.__str__(), "Queen Street (West) - 1")


class RestrictedParkingByLawModelTest(ByLawModelTest):
    @classmethod
    def setUpTestData(cls):
        highway = Highway.objects.create(name="queen street", street_end="W")
        cross_street_1 = Highway.objects.create(name="dowling avenue", street_end="W")
        cross_street_2 = Highway.objects.create(name="jameson avenue", street_end="W")

        intersection_1 = Intersection.objects.create(
            main_street=highway,
            cross_street=cross_street_1,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )
        intersection_2 = Intersection.objects.create(
            main_street=highway,
            cross_street=cross_street_2,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )
        # setup objects used by all test methods
        RestrictedParkingByLaw.objects.create(
            source_id="1",
            schedule="15",
            schedule_name="Parking for Restricted Periods",
            highway=highway,
            side="North",
            between="Glenholme Avenue and Oakwood Avenue",
            times_and_or_days="10:00 a.m. to 6:00 p.m., Mon. to Fri.",
            max_period_permitted="12 hours",
            boundary_start=intersection_1,
            boundary_end=intersection_2,
        )

    def test_source_id(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("source_id").verbose_name
        self.assertEqual(field_label, "source id")

    def test_schedule_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule").verbose_name
        self.assertEqual(field_label, "schedule")

    def test_schedule_name_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("schedule_name").verbose_name
        self.assertEqual(field_label, "schedule name")

    def test_highway_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("highway").verbose_name
        self.assertEqual(field_label, "highway")

    def test_side_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("side").verbose_name
        self.assertEqual(field_label, "side")

    def test_between_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("between").verbose_name
        self.assertEqual(field_label, "between")

    def test_times_and_or_day_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("times_and_or_days").verbose_name
        self.assertEqual(field_label, "times and or days")

    def test_max_period_permitted_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("max_period_permitted").verbose_name
        self.assertEqual(field_label, "max period permitted")

    def test_boundary_start_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_start").verbose_name
        self.assertEqual(field_label, "boundary start")

    def test_boundary_end_label(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        field_label = law._meta.get_field("boundary_end").verbose_name
        self.assertEqual(field_label, "boundary end")

    def test_str_method(self):
        law = RestrictedParkingByLaw.objects.get(id=1)
        self.assertEqual(law.__str__(), "Ashbury Avenue (North) - 1")


class HighwayModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # setup objects used by all test methods
        Highway.objects.create(name="king street", street_end="W")

    def test_name_label(self):
        highway = Highway.objects.get(id=1)
        field_label = highway._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_street_end_label(self):
        highway = Highway.objects.get(id=1)
        field_label = highway._meta.get_field("street_end").verbose_name
        self.assertEqual(field_label, "street end")

    def test_str_method(self):
        highway = Highway.objects.get(id=1)
        self.assertEqual(highway.__str__(), "king street W")


class IntersectionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls, self):
        # setup objects used by all test methods
        main_street = Highway.objects.create(name="king street", street_end="W")
        cross_street = Highway.objects.create(name="dowling avenue", street_end="W")

        self.intersection = Intersection.objects.create(
            main_street=main_street,
            cross_street=cross_street,
            lat=-90.5203,
            lng=29.5233,
            status="FNF",
        )

    def test_main_street_label(self):
        field_label = self.intersection._meta.get_field("main_street").verbose_name
        self.assertEqual(field_label, "main street")

    def test_cross_street_label(self):
        field_label = self.intersection._meta.get_field("cross_street").verbose_name
        self.assertEqual(field_label, "cross street")

    def test_lat_label(self):
        field_label = self.intersection._meta.get_field("lat").verbose_name
        self.assertEqual(field_label, "lat")

    def test_lng_label(self):
        field_label = self.intersection._meta.get_field("lng").verbose_name
        self.assertEqual(field_label, "lng")

    def test_status_label(self):
        field_label = self.intersection._meta.get_field("status").verbose_name
        self.assertEqual(field_label, "status")

    def test_str_method(self):
        main = self.intersection.main_street.name
        cross = self.intersection.cross_street.name
        status = self.intersection.status
        self.assertEqual(self.intersection.__str__(), f"{main} at {cross} ({status})")
