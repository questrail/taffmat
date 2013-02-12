import filecmp
import os
import re
import unittest

import numpy as np

import taffmat

class TestPrintingExponentNotation(unittest.TestCase):

    def test_printing_exponent_notation(self):
        numbers_to_test = [0.00002, 0.00004, 0.00008, 0.0002, 0.0004,
                0.0008, 0.002]
        number_as_string = [taffmat._format_exponent_notation(number_to_convert, 6, 3)
                for number_to_convert in numbers_to_test]
        correct_representation = ['2.000000e-005', '4.000000e-005', '8.000000e-005',
                '2.000000e-004', '4.000000e-004', '8.000000e-004', '2.000000e-003']
        self.assertEqual(number_as_string,correct_representation)

class TestConvertingDataArray(unittest.TestCase):

    def setUp(self):
        self.given_data_array_int = np.array([[-25000, -12500, 0, 1, 12500, 25000],
                [-25000, -12500, 0, 1, 12500, 25000]], dtype=np.int16)
        self.number_of_series = 2
        self.slope = [8e-05, 0.0002]
        self.y_offset = [0.0, 0.1]
        self.given_data_array_float = np.array(
                [[-2.0, -1.0, 0.0, 0.00008, 1.0, 2.0],
                [-4.9, -2.4, 0.1, 0.1002, 2.6, 5.1]], dtype=np.float64)

    def test_converting_data_array_from_int_to_float(self):
        data_array_float = taffmat._apply_slope_and_offset(
                self.given_data_array_int, self.number_of_series,
                self.slope, self.y_offset)
        np.testing.assert_array_almost_equal(data_array_float, self.given_data_array_float,
                decimal=8,
                err_msg='Failed applying slope and offset')

    def test_converting_data_array_from_float_to_int(self):
        data_array_int = taffmat._remove_slope_and_offset(
                self.given_data_array_float, self.number_of_series,
                self.slope, self.y_offset)
        np.testing.assert_array_equal(data_array_int, self.given_data_array_int,
                'Failed removing slope and offset')

class TestInputFilenames(unittest.TestCase):

    def setUp(self):
        self.test_taffmat_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'test_taffmat_files')

        known_data_array_input_file = os.path.join(
                self.test_taffmat_directory, 'utest001_data_array_float64.npy')
        self.known_data_array = np.load(known_data_array_input_file)

    def test_nonexistent_input_file(self):
        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(
                self.test_taffmat_directory,
                'nonexistent_taffmat_file.DAT')
        self.assertFalse(
                taffmat.read_taffmat(input_file_basename))

    def test_input_file_with_dat_extension(self):
        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(
                self.test_taffmat_directory,
                'UTEST001.DAT')
        data_array, time_vector, header_data = \
                taffmat.read_taffmat(input_file_basename)
        np.testing.assert_array_equal(data_array,self.known_data_array,
                'Incorrectly read data_array using filename with .DAT extension')

    def test_input_file_without_extension(self):
        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(
                self.test_taffmat_directory,
                'UTEST001.DAT')
        data_array, time_vector, header_data = \
                taffmat.read_taffmat(input_file_basename)
        np.testing.assert_array_equal(data_array,self.known_data_array,
                'Incorrectly read data_array using filename without an extension')

class TestReadingTAFFmatFile(unittest.TestCase):

    def setUp(self):
        test_taffmat_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'test_taffmat_files')

        # Read in the TAFFmat file under test
        input_file_basename = os.path.join(
                test_taffmat_directory,
                'UTEST001')
        self.data_array, self.time_vector, self.header_data = \
                taffmat.read_taffmat(input_file_basename)
        self.beginning_of_raw_data_array = np.array([2959, 6291, 9386, 12121],
                dtype=np.int16)

        # Read in the known data array and provide the answers
        # for the header file. By having this setup here, we can
        # change to a different test file by simply updating
        # this section instead of searching all through the test code
        known_data_array_input_file = os.path.join(
                test_taffmat_directory, 'utest001_data_array_float64.npy')
        self.known_data_array = np.load(known_data_array_input_file)
        self.known_header = {}
        self.known_header['sampling_frequency_hz'] = 96000
        self.known_header['number_of_series'] = 2
        self.known_header['slope'] = [8e-05, 0.0002]

    def test_sampling_frequency(self):
        self.assertEqual(self.header_data['sampling_frequency_hz'],
                self.known_header['sampling_frequency_hz'],
                'Incorrect sampling frequency. Found {fs}, expected {known_fs}'.format(
                    fs = self.header_data['sampling_frequency_hz'],
                    known_fs = self.known_header['sampling_frequency_hz']))

    def test_number_of_data_samples(self):
        print(self.data_array.shape)
        print(self.known_data_array.shape)
        self.assertEqual(self.data_array.shape,self.known_data_array.shape,
                'data_array.shape = {data_shape} but should have been {known_shape}'.format(
                    data_shape = self.data_array.shape,
                    known_shape = self.known_data_array.shape))

    def test_number_of_data_samples_against_header(self):
        self.assertEqual(self.header_data['number_of_samples'],
                self.data_array.shape[1],
                'Mismatched number of samples between header file and data_array')

    def test_number_of_time_samples(self):
        self.assertEqual(self.data_array.shape[1],
                self.time_vector.shape[0],
                'Incorrect number of samples in time_vector')

    def test_number_of_series(self):
        self.assertEqual(self.header_data['number_of_series'], 
                self.known_header['number_of_series'],
                'Incorrect number of series read from header file')

    def test_series_1_slope(self):
        self.assertEqual(self.header_data['slope'][0], 
                self.known_header['slope'][0],
                'Incorrect slope for channel 1')

    def test_data_array_was_read_correctly(self):
        np.testing.assert_array_equal(self.data_array,self.known_data_array,
                'data_array was not read correctly')

    def test_data_conversion_from_int_to_float(self):
        self.assertAlmostEqual(self.data_array[0,0],
                (self.beginning_of_raw_data_array[0] * self.header_data['slope'][0]),
                msg='Incorrect conversion from int16 data to float')

class TestWritingTAFFmatFile(unittest.TestCase):

    def setUp(self):
        self.test_taffmat_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'test_taffmat_files')

        # Read in the TAFFmat file under test
        self.input_base_filename = os.path.join(
                self.test_taffmat_directory, 'UTEST001')
        self.data_array, self.time_vector, self.header_data = \
                taffmat.read_taffmat(self.input_base_filename)

        # Setup the output_basefilename
        self.output_base_filename = os.path.join(
                self.test_taffmat_directory, 'test_output_taffmat')

        # Write the .dat and .hdr files using taffmat.py
        taffmat.write_taffmat(self.data_array, self.header_data, self.output_base_filename)

    def tearDown(self):
        # Need to delete the test output file
        output_dat_filename = '{base}.dat'.format(base=self.output_base_filename)
        output_hdr_filename = '{base}.hdr'.format(base=self.output_base_filename)
        try:
            os.remove(output_dat_filename)
        except:
            print("Couldn't remove the test dat file.")

        try:
            os.remove(output_hdr_filename)
        except:
            print("Couldn't remove the test hdr file.")

    def _get_dat_hdr_filenames_from_base(self, base_filename):
        dat_filename = '{base}.dat'.format(base=base_filename)
        hdr_filename = '{base}.hdr'.format(base=base_filename)
        return dat_filename, hdr_filename

    def test_writing_data_array(self):
        source_dat, source_hdr = self._get_dat_hdr_filenames_from_base(self.input_base_filename)
        output_dat, output_hdr = self._get_dat_hdr_filenames_from_base(self.output_base_filename)
        data_files_equal = filecmp.cmp(source_dat, output_dat, shallow=False)
        self.assertTrue(data_files_equal,
                'Saved dat file does not equal source dat file.')

    def test_writing_header_file(self):
        '''
        Compare the header file written using taffmat.py against the original
        TAFFmat header file created by the LX-10
        '''
        source_dat, source_hdr = self._get_dat_hdr_filenames_from_base(self.input_base_filename)
        output_dat, output_hdr = self._get_dat_hdr_filenames_from_base(self.output_base_filename)
        with open(source_hdr, 'r') as hdr_source_file:
            source_hdr_contents = hdr_source_file.read()
        with open(output_hdr, 'r') as hdr_output_file:
            output_hdr_contents = hdr_output_file.read()
        # FIXME: Instead of stripping out all blank lines, I should probably
        # only strip out blank lines that are at the end of the TAFFmat hdr file.
        source_hdr_contents_no_blank_lines = filter(
                lambda x: not re.match(r'^\s*$', x), source_hdr_contents)
        output_hdr_contents_no_blank_lines = filter(
                lambda x: not re.match(r'^\s*$', x), output_hdr_contents)
        self.assertEqual(source_hdr_contents_no_blank_lines,
                output_hdr_contents_no_blank_lines,
                'Source and output header files are not the same (excluding blank lines).')

class TestWritingTAFFmatFileSlice(unittest.TestCase):

    def setUp(self):
        self.test_taffmat_directory = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                'test_taffmat_files')

        # Read in the TAFFmat file under test
        self.input_base_filename = os.path.join(
                self.test_taffmat_directory, 'UTEST001')
        self.data_array, self.time_vector, self.header_data = \
                taffmat.read_taffmat(self.input_base_filename)

    def test_writing_dat_file_slice(self):
        '''
        Write the first 1000 elements of data_array to a new .dat and .hdr file.
        Then read the new .dat file and make sure it matches the first 1000
        elements of the original data_array
        '''

        slice_output_base_filename = os.path.join(
                self.test_taffmat_directory, 'test_slice_output_taffmat')

        #number_of_samples_in_slice = self.data_array.shape[1]
        number_of_samples_in_slice = 1000
        original_data_array = np.copy(self.data_array[:,0:number_of_samples_in_slice])

        # Write the TAFFmat data slice
        taffmat.write_taffmat_slice(self.data_array, self.header_data,
                slice_output_base_filename, 0, number_of_samples_in_slice-1)

        # Read the TAFFmat data slice
        slice_data_array, slice_time_vector, slice_header_data = \
                taffmat.read_taffmat(slice_output_base_filename)

        # Confirm the proper number of samples exist
        self.assertEqual(slice_data_array.shape[1],number_of_samples_in_slice,
                'Number of samples in slice incorrect.')

        np.testing.assert_array_equal(slice_data_array,
                original_data_array,
                'The sliced data array does not equal the original data array.')


if __name__ == '__main__':
    unittest.main()

