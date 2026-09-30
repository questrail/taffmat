# Try to future proof code so that it's Python 3.x ready

# Imports from the Python Standard Library
import copy
import filecmp
import os
import tempfile
import unittest

# Other imports
import numpy as np

import taffmat


class TestPrintingExponentNotation(unittest.TestCase):
    def test_printing_exponent_notation(self):
        numbers_to_test = (0.00002, 0.00004, 0.00008, 0.0002, 0.0004, 0.0008, 0.002)
        number_as_string = [
            taffmat._format_exponent_notation(number_to_convert, 6, 3)
            for number_to_convert in numbers_to_test
        ]
        correct_representation = [
            "2.000000e-005",
            "4.000000e-005",
            "8.000000e-005",
            "2.000000e-004",
            "4.000000e-004",
            "8.000000e-004",
            "2.000000e-003",
        ]
        self.assertEqual(number_as_string, correct_representation)


class TestConvertingDataArray(unittest.TestCase):
    def setUp(self):
        self.given_data_array_int = np.array(
            [
                [-25000, -12500, 0, 1, 12500, 25000],
                [-25000, -12500, 0, 1, 12500, 25000],
            ],
            dtype=np.int16,
        )
        self.number_of_series = 2
        self.slope = [8e-05, 0.0002]
        self.y_offset = [0.0, 0.1]
        self.given_data_array_float = np.array(
            [[-2.0, -1.0, 0.0, 0.00008, 1.0, 2.0], [-4.9, -2.4, 0.1, 0.1002, 2.6, 5.1]],
            dtype=np.float64,
        )
        self.given_data_array_new_slope = np.array(
            [[-1.0, -0.5, 0.0, 0.00004, 0.5, 1.0], [-4.9, -2.4, 0.1, 0.1002, 2.6, 5.1]],
            dtype=np.float64,
        )

    def test_converting_data_array_from_int_to_float(self):
        data_array_float = taffmat._apply_slope_and_offset(
            self.given_data_array_int, self.number_of_series, self.slope, self.y_offset
        )
        np.testing.assert_array_almost_equal(
            data_array_float,
            self.given_data_array_float,
            decimal=8,
            err_msg="Failed applying slope and offset",
        )

    def test_converting_data_array_from_float_to_int(self):
        data_array_int = taffmat._remove_slope_and_offset(
            self.given_data_array_float,
            self.number_of_series,
            self.slope,
            self.y_offset,
        )
        np.testing.assert_array_equal(
            data_array_int,
            self.given_data_array_int,
            "Failed removing slope and offset",
        )

    def test_changing_slope(self):
        data_array_new_slope = taffmat.change_slope(self.given_data_array_float, 0, 0.5)
        np.testing.assert_array_equal(
            data_array_new_slope,
            self.given_data_array_new_slope,
            "Failed applying 1/2 gain to slope of series 0",
        )
        np.testing.assert_array_equal(
            self.given_data_array_float, self.given_data_array_new_slope
        )


class TestInputFilenames(unittest.TestCase):
    def setUp(self):
        self.test_taffmat_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_taffmat_files"
        )

        known_data_array_input_file = os.path.join(
            self.test_taffmat_directory, "utest001_data_array_float64.npy"
        )
        self.known_data_array = np.load(known_data_array_input_file)

    def test_nonexistent_input_file(self):
        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(
            self.test_taffmat_directory, "nonexistent_taffmat_file.DAT"
        )
        with self.assertRaises(FileNotFoundError):
            taffmat.read_taffmat(input_file_basename)

    def test_input_file_with_dat_extension(self):
        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(self.test_taffmat_directory, "UTEST001.DAT")
        data_array, _time_vector, _header_data = taffmat.read_taffmat(
            input_file_basename
        )
        np.testing.assert_array_equal(
            data_array,
            self.known_data_array,
            "Incorrectly read data_array using filename with .DAT extension",
        )

    def test_input_file_without_extension(self):
        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(self.test_taffmat_directory, "UTEST001")
        data_array, _time_vector, _header_data = taffmat.read_taffmat(
            input_file_basename
        )
        np.testing.assert_array_equal(
            data_array,
            self.known_data_array,
            "Incorrectly read data_array using filename without an extension",
        )


class TestReadingTAFFmatFile(unittest.TestCase):
    def setUp(self):
        test_taffmat_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_taffmat_files"
        )

        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(test_taffmat_directory, "UTEST001")
        self.data_array, self.time_vector, self.header_data = taffmat.read_taffmat(
            input_file_basename
        )
        self.beginning_of_raw_data_array = np.array(
            [2959, 6291, 9386, 12121], dtype=np.int16
        )

        # Read in the known data array and provide the answers
        # for the header file. By having this setup here, we can
        # change to a different test file by simply updating
        # this section instead of searching all through the test code
        known_data_array_input_file = os.path.join(
            test_taffmat_directory, "utest001_data_array_float64.npy"
        )
        self.known_data_array = np.load(known_data_array_input_file)
        self.known_header = {}
        self.known_header["sampling_frequency_hz"] = 96000
        self.known_header["number_of_series"] = 2
        self.known_header["slope"] = [8e-05, 0.0002]

    def test_sampling_frequency(self):
        self.assertEqual(
            self.header_data["sampling_frequency_hz"],
            self.known_header["sampling_frequency_hz"],
            "Incorrect sampling frequency. Found {fs}, expected {known_fs}".format(
                fs=self.header_data["sampling_frequency_hz"],
                known_fs=self.known_header["sampling_frequency_hz"],
            ),
        )

    def test_number_of_data_samples(self):
        self.assertEqual(
            self.data_array.shape,
            self.known_data_array.shape,
            f"data_array.shape = {self.data_array.shape} but should have "
            f" been {self.known_data_array.shape}",
        )

    def test_number_of_data_samples_against_header(self):
        self.assertEqual(
            self.header_data["number_of_samples"],
            self.data_array.shape[1],
            "Mismatched number of samples between header file and data_array",
        )

    def test_number_of_time_samples(self):
        self.assertEqual(
            self.data_array.shape[1],
            self.time_vector.shape[0],
            "Incorrect number of samples in time_vector",
        )

    def test_time_vector_starts_at_zero(self):
        self.assertEqual(
            self.time_vector[0], 0, "time_vector should start at the first sample"
        )

    def test_time_vector_steps_by_one_sampling_period(self):
        # Sample n was taken at n / sampling_frequency_hz, so every step is one
        # sampling period. Spreading the samples over number_of_samples / fs
        # instead stretched every step by a factor of N / (N - 1).
        sampling_period_sec = 1 / self.known_header["sampling_frequency_hz"]
        np.testing.assert_allclose(
            np.diff(self.time_vector),
            sampling_period_sec,
            err_msg="time_vector should step by one sampling period",
        )

    def test_time_vector_ends_one_sample_short_of_the_duration(self):
        # The last of N samples was taken at (N - 1) / fs; the recording runs
        # one sampling period past it. Putting that sample at N / fs left every
        # sample progressively late, by a full sample at the end of the
        # recording.
        num_samples = self.header_data["number_of_samples"]
        sampling_period_sec = 1 / self.known_header["sampling_frequency_hz"]
        self.assertAlmostEqual(
            self.time_vector[-1],
            (num_samples - 1) * sampling_period_sec,
            msg="time_vector should end one sampling period short of the duration",
        )

    def test_time_vector_agrees_with_times_taken_from_a_sample_index(self):
        # A caller that works a time out from a sample index and the sampling
        # frequency has to land on the same instant this vector reports.
        sampling_frequency_hz = self.known_header["sampling_frequency_hz"]
        for index in (0, 1, 1000, self.header_data["number_of_samples"] - 1):
            self.assertAlmostEqual(
                self.time_vector[index],
                index / sampling_frequency_hz,
                msg=f"time_vector disagrees at sample {index}",
            )

    def test_number_of_series(self):
        self.assertEqual(
            self.header_data["number_of_series"],
            self.known_header["number_of_series"],
            "Incorrect number of series read from header file",
        )

    def test_series_1_slope(self):
        self.assertEqual(
            self.header_data["slope"][0],
            self.known_header["slope"][0],
            "Incorrect slope for channel 1",
        )

    def test_data_array_was_read_correctly(self):
        np.testing.assert_array_equal(
            self.data_array, self.known_data_array, "data_array was not read correctly"
        )

    def test_data_conversion_from_int_to_float(self):
        self.assertAlmostEqual(
            self.data_array[0, 0],
            (self.beginning_of_raw_data_array[0] * self.header_data["slope"][0]),
            msg="Incorrect conversion from int16 data to float",
        )


class TestWritingTAFFmatFile(unittest.TestCase):
    def setUp(self):
        self.test_taffmat_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_taffmat_files"
        )

        # Read in the TAFFmat file under test
        self.input_base_filename = os.path.join(self.test_taffmat_directory, "UTEST001")
        self.data_array, self.time_vector, self.header_data = taffmat.read_taffmat(
            self.input_base_filename
        )

        # Setup the output_basefilename
        self.output_base_filename = os.path.join(
            self.test_taffmat_directory, "test_output_taffmat"
        )

        # Write the .dat and .hdr files using taffmat.py
        taffmat.write_taffmat(
            self.data_array, self.header_data, self.output_base_filename
        )

    def tearDown(self):
        # Need to delete the test output file
        output_dat_filename = f"{self.output_base_filename}.DAT"
        output_hdr_filename = f"{self.output_base_filename}.HDR"
        try:
            os.remove(output_dat_filename)
        except OSError as error:
            print(error)
            print("Couldn't remove the test dat file.")

        try:
            os.remove(output_hdr_filename)
        except OSError as error:
            print(error)
            print("Couldn't remove the test hdr file.")

    def _get_dat_hdr_filenames_from_base(self, base_filename):
        dat_filename = f"{base_filename}.DAT"
        hdr_filename = f"{base_filename}.HDR"
        return dat_filename, hdr_filename

    def test_writing_data_array(self):
        source_dat, _source_hdr = self._get_dat_hdr_filenames_from_base(
            self.input_base_filename
        )
        output_dat, _output_hdr = self._get_dat_hdr_filenames_from_base(
            self.output_base_filename
        )
        data_files_equal = filecmp.cmp(source_dat, output_dat, shallow=False)
        self.assertTrue(
            data_files_equal, "Saved dat file does not equal source dat file."
        )

    def test_writing_header_file_and_compare_with_original_taffmat(self):
        _source_dat, source_hdr = self._get_dat_hdr_filenames_from_base(
            self.input_base_filename
        )
        _output_dat, output_hdr = self._get_dat_hdr_filenames_from_base(
            self.output_base_filename
        )
        # newline="" keeps the \r\n the split relies on. Without it Windows
        # reads each line ending as \n, leaving one element per file and
        # nothing after [1:] to compare.
        with open(source_hdr, newline="") as hdr_source_file:
            source_hdr_contents = hdr_source_file.read().split("\r\n")
        with open(output_hdr, newline="") as hdr_output_file:
            output_hdr_contents = hdr_output_file.read().split("\r\n")
        source_hdr_contents_no_whitespace = [s.strip() for s in source_hdr_contents]
        output_hdr_contents_no_whitespace = [s.strip() for s in output_hdr_contents]
        self.assertEqual(
            source_hdr_contents_no_whitespace[1:], output_hdr_contents_no_whitespace[1:]
        )

    def test_writing_different_dataset_filename(self):
        new_output_base_filename = "something_different"
        taffmat.write_taffmat(
            self.data_array, self.header_data, new_output_base_filename
        )
        _data_array, _time_vector, header_data = taffmat.read_taffmat(
            new_output_base_filename
        )
        self.assertEqual(header_data["dataset"], new_output_base_filename.upper())
        new_output_dat, new_output_hdr = self._get_dat_hdr_filenames_from_base(
            new_output_base_filename
        )
        try:
            os.remove(new_output_dat)
        except OSError as error:
            print(error)
            print("Couldn't remove the test dat file.")

        try:
            os.remove(new_output_hdr)
        except OSError as error:
            print(error)
            print("Couldn't remove the test hdr file.")


class TestWritingTAFFmatFileSlice(unittest.TestCase):
    def setUp(self):
        self.test_taffmat_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_taffmat_files"
        )

        # Read in the TAFFmat file under test
        self.input_base_filename = os.path.join(self.test_taffmat_directory, "UTEST001")
        self.data_array, self.time_vector, self.header_data = taffmat.read_taffmat(
            self.input_base_filename
        )

    def test_writing_dat_file_slice(self):
        """
        Write the first 1000 elements of data_array to a new .dat and .hdr
        file.  Then read the new .dat file and make sure it matches the first
        1000 elements of the original data_array
        """

        slice_output_base_filename = os.path.join(
            self.test_taffmat_directory, "test_slice_output_taffmat"
        )

        # number_of_samples_in_slice = self.data_array.shape[1]
        number_of_samples_in_slice = 1000
        original_data_array = np.copy(self.data_array[:, 0:number_of_samples_in_slice])

        # Write the TAFFmat data slice
        taffmat.write_taffmat_slice(
            self.data_array,
            self.header_data,
            slice_output_base_filename,
            0,
            number_of_samples_in_slice - 1,
        )

        # Read the TAFFmat data slice
        slice_data_array, _slice_time_vector, _slice_header_data = taffmat.read_taffmat(
            slice_output_base_filename
        )

        # Confirm the proper number of samples exist
        self.assertEqual(
            slice_data_array.shape[1],
            number_of_samples_in_slice,
            "Number of samples in slice incorrect.",
        )

        np.testing.assert_array_equal(
            slice_data_array,
            original_data_array,
            "The sliced data array does not equal the original data array.",
        )

    def test_writing_a_slice_leaves_the_given_header_alone(self):
        """
        The header describes the recording the slice was cut from, and the
        caller keeps using it after the slice is written. Describing the
        slice must not overwrite it, or a caller asking how long the
        recording was gets the length of the slice back instead.
        """

        slice_output_base_filename = os.path.join(
            self.test_taffmat_directory, "test_slice_output_taffmat"
        )
        header_before = copy.deepcopy(self.header_data)

        taffmat.write_taffmat_slice(
            self.data_array, self.header_data, slice_output_base_filename, 0, 999
        )

        self.assertEqual(
            self.header_data["number_of_samples"],
            header_before["number_of_samples"],
            "Writing a slice changed the recording's sample count.",
        )
        self.assertEqual(
            self.header_data["voice_memo_on"],
            header_before["voice_memo_on"],
            "Writing a slice turned off the recording's voice memo.",
        )
        self.assertEqual(
            self.header_data["dataset"],
            header_before["dataset"],
            "Writing a slice renamed the recording's dataset.",
        )

    def test_writing_a_slice_leaves_the_given_data_array_alone(self):
        slice_output_base_filename = os.path.join(
            self.test_taffmat_directory, "test_slice_output_taffmat"
        )
        data_array_before = np.copy(self.data_array)

        taffmat.write_taffmat_slice(
            self.data_array, self.header_data, slice_output_base_filename, 0, 999
        )

        np.testing.assert_array_equal(
            self.data_array,
            data_array_before,
            "Writing a slice changed the data array it was given.",
        )

    def test_the_slice_header_describes_the_slice(self):
        """
        The copy taken to protect the caller still has to carry the sample
        count and the dropped voice memo through to the .hdr file.
        """

        slice_output_base_filename = os.path.join(
            self.test_taffmat_directory, "test_slice_output_taffmat"
        )
        number_of_samples_in_slice = 1000

        taffmat.write_taffmat_slice(
            self.data_array,
            self.header_data,
            slice_output_base_filename,
            0,
            number_of_samples_in_slice - 1,
        )

        _data_array, _time_vector, slice_header_data = taffmat.read_taffmat(
            slice_output_base_filename
        )

        self.assertEqual(
            slice_header_data["number_of_samples"], number_of_samples_in_slice
        )
        self.assertFalse(slice_header_data["voice_memo_on"])
        # The DATASET line is written from the output filename rather than
        # from the header, so the slice is named after the file it lands in
        # without the caller's header having to be renamed to say so.
        self.assertEqual(
            slice_header_data["dataset"],
            os.path.basename(slice_output_base_filename).upper(),
        )


class TestVoiceMemoRecording(unittest.TestCase):
    """
    UTEST001 was recorded without a voice memo, so reading and writing the
    VOICE_MEMO line went unexercised, as did dropping it when writing a
    slice. Build a recording that claims one by writing it out.
    """

    def setUp(self):
        self.test_taffmat_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_taffmat_files"
        )
        self.written_base_filenames = []

        input_base_filename = os.path.join(self.test_taffmat_directory, "UTEST001")
        self.data_array, _time_vector, header_data = taffmat.read_taffmat(
            input_base_filename
        )

        header_data["voice_memo_on"] = True
        header_data["voice_memo_bits_per_sample"] = "8"
        header_data["voice_memo_size_bytes"] = 1234
        self.header_data = header_data

    def tearDown(self):
        for base_filename in self.written_base_filenames:
            for extension in (".DAT", ".HDR"):
                try:
                    os.remove(base_filename + extension)
                except OSError as error:
                    print(error)
                    print(f"Couldn't remove {base_filename}{extension}.")

    def _output_base_filename(self, name):
        base_filename = os.path.join(self.test_taffmat_directory, name)
        self.written_base_filenames.append(base_filename)
        return base_filename

    def test_a_voice_memo_survives_a_write_and_read(self):
        base_filename = self._output_base_filename("test_voice_memo_taffmat")

        taffmat.write_taffmat(self.data_array, self.header_data, base_filename)
        _data_array, _time_vector, header_data = taffmat.read_taffmat(base_filename)

        self.assertTrue(header_data["voice_memo_on"])
        self.assertEqual(
            header_data["voice_memo_bits_per_sample"],
            self.header_data["voice_memo_bits_per_sample"],
        )
        self.assertEqual(
            header_data["voice_memo_size_bytes"],
            self.header_data["voice_memo_size_bytes"],
        )

    def test_a_slice_drops_the_voice_memo_without_disowning_the_original(self):
        """
        The memo no longer matches the length of the data, so the slice is
        written without it; the recording it was cut from still has one.
        """

        recording = self._output_base_filename("test_voice_memo_taffmat")
        taffmat.write_taffmat(self.data_array, self.header_data, recording)
        data_array, _time_vector, header_data = taffmat.read_taffmat(recording)

        slice_base_filename = self._output_base_filename("test_voice_memo_slice")
        taffmat.write_taffmat_slice(
            data_array, header_data, slice_base_filename, 0, 999
        )

        _slice_data, _slice_time, slice_header = taffmat.read_taffmat(
            slice_base_filename
        )
        self.assertFalse(slice_header["voice_memo_on"])
        self.assertTrue(
            header_data["voice_memo_on"],
            "Writing a slice turned off the recording's voice memo.",
        )


class TestWritingLeavesTheDataFaithful(unittest.TestCase):
    """
    What write_taffmat puts on disk, and what it leaves in the caller's hands,
    has to be the recording it was given.
    """

    def setUp(self):
        test_taffmat_directory = os.path.join(
            os.path.dirname(os.path.realpath(__file__)), "test_taffmat_files"
        )
        self.data_array, _time_vector, self.header_data = taffmat.read_taffmat(
            os.path.join(test_taffmat_directory, "UTEST001")
        )
        output_directory = tempfile.TemporaryDirectory()
        self.addCleanup(output_directory.cleanup)
        self.output_base_filename = os.path.join(output_directory.name, "OUTPUT")

    def test_writing_leaves_the_given_data_array_alone(self):
        """
        The caller's array held measured values and has to keep holding them.
        Converting it to ADC codes in place handed a caller that went on
        analysing, or wrote it a second time, integers such as 2959.0 where
        0.23672 V had been.
        """
        data_array_before = np.copy(self.data_array)

        taffmat.write_taffmat(
            self.data_array, self.header_data, self.output_base_filename
        )

        np.testing.assert_array_equal(
            self.data_array,
            data_array_before,
            "Writing changed the data array it was given.",
        )

    def test_writing_the_same_data_twice_writes_the_same_file(self):
        first_base_filename = self.output_base_filename + "_FIRST"
        taffmat.write_taffmat(self.data_array, self.header_data, first_base_filename)
        taffmat.write_taffmat(
            self.data_array, self.header_data, self.output_base_filename
        )

        self.assertTrue(
            filecmp.cmp(
                f"{first_base_filename}.DAT",
                f"{self.output_base_filename}.DAT",
                shallow=False,
            ),
            "A second write of the same data wrote a different .dat file.",
        )

    def test_a_value_beyond_the_adc_range_is_refused_rather_than_wrapped(self):
        """
        Doubling channel 1 pushes its peak past +32,767 codes. Cast straight
        to int16 it wrapped around, and 2.82 V was read back as -2.42 V.
        """
        doubled = taffmat.change_slope(np.copy(self.data_array), 0, 2)

        with self.assertRaisesRegex(ValueError, "series 0"):
            taffmat.write_taffmat(doubled, self.header_data, self.output_base_filename)

    def test_a_value_that_is_not_finite_is_refused(self):
        self.data_array[1, 10] = np.nan

        with self.assertRaisesRegex(ValueError, "series 1, sample 10"):
            taffmat.write_taffmat(
                self.data_array, self.header_data, self.output_base_filename
            )

    def test_refusing_the_data_leaves_no_files_behind(self):
        """
        A .hdr written ahead of a .dat that could not be would look to the
        next reader like a recording with its data missing.
        """
        doubled = taffmat.change_slope(np.copy(self.data_array), 0, 2)

        with self.assertRaises(ValueError):
            taffmat.write_taffmat(doubled, self.header_data, self.output_base_filename)

        self.assertFalse(os.path.exists(f"{self.output_base_filename}.HDR"))
        self.assertFalse(os.path.exists(f"{self.output_base_filename}.DAT"))

    def test_a_long_file_survives_a_write_and_read(self):
        """
        A LONG header promises 4-byte samples. Writing int16 regardless read
        back as half as many samples, each built from two of the originals.
        """
        self.header_data["file_type"] = "LONG"

        taffmat.write_taffmat(
            self.data_array, self.header_data, self.output_base_filename
        )
        data_array, _time_vector, header_data = taffmat.read_taffmat(
            self.output_base_filename
        )

        self.assertEqual(
            os.path.getsize(f"{self.output_base_filename}.DAT"),
            header_data["number_of_samples"] * header_data["number_of_series"] * 4,
        )
        np.testing.assert_array_equal(data_array, self.data_array)

    def test_a_long_file_holds_codes_beyond_the_int16_range(self):
        self.header_data["file_type"] = "LONG"
        doubled = taffmat.change_slope(np.copy(self.data_array), 0, 2)

        taffmat.write_taffmat(doubled, self.header_data, self.output_base_filename)
        data_array, _time_vector, _header_data = taffmat.read_taffmat(
            self.output_base_filename
        )

        np.testing.assert_allclose(data_array, doubled)

    def test_header_lines_end_in_a_single_crlf(self):
        """
        The writer ends each line in \\r\\n itself. In text mode Windows
        translated the \\n again, ending every line in \\r\\r\\n.
        """
        taffmat.write_taffmat(
            self.data_array, self.header_data, self.output_base_filename
        )

        with open(f"{self.output_base_filename}.HDR", "rb") as hdr_file:
            raw_header = hdr_file.read()

        self.assertTrue(raw_header.endswith(b"\r\n"))
        for line in raw_header.split(b"\r\n"):
            self.assertNotIn(b"\r", line, "A header line has a stray \\r.")
            self.assertNotIn(b"\n", line, "A header line has a bare \\n.")


if __name__ == "__main__":
    unittest.main()
