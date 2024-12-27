rm ../data/csv/IMPtime.csv
rm ../data/csv/OMPtime.csv
rm ../data/csv/SEQtime.csv

echo "Matrix size 2^4:"
./matTrans 4
echo
echo

echo "Matrix size 2^5:"
./matTrans 5
echo
echo

echo "Matrix size 2^6:"
./matTrans 6
echo
echo

echo "Matrix size 2^7:"
./matTrans 7
echo
echo

echo "Matrix size 2^8:"
./matTrans 8
echo
echo

echo "Matrix size 2^9:"
./matTrans 9
echo
echo

echo "Matrix size 2^10:"
./matTrans 10
echo
echo

echo "Matrix size 2^11:"
./matTrans 11
echo
echo

echo "Matrix size 2^12:"
./matTrans 12
echo
echo