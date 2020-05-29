# echo "rakvere"
# echo "all"
aws lambda invoke --cli-read-timeout 600 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"rakvere","deal_type":"all","room_nr":"all"}' outfile.txt
start=`date +%s`
echo "tartu"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":1,"room_nr":1}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tartu"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":1,"room_nr":2}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tartu"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":1,"room_nr":3}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.



start=`date +%s`
echo "tartu"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":1,"room_nr":4}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tartu"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":1,"room_nr":5}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tartu"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":2,"room_nr":1}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.

start=`date +%s`
echo "tartu"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":2,"room_nr":2}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tartu"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":2,"room_nr":2}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.

start=`date +%s`
echo "tartu"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":2,"room_nr":4}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.

start=`date +%s`
echo "tartu"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tartu","deal_type":2,"room_nr":5}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.

start=`date +%s`
echo "tallinn"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":1,"room_nr":2}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.

start=`date +%s`
echo "tallinn"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":1,"room_nr":1}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tallinn"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":1,"room_nr":3}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.



start=`date +%s`
echo "tallinn"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":1,"room_nr":4}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


start=`date +%s`
echo "tallinn"
echo "1"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":1,"room_nr":5}' outfile.txt
end=`date +%s`
echo Execution time was `expr $end - $start` seconds.



echo "tallinn"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":2,"room_nr":1}' outfile.txt

end=`date +%s`
echo Execution time was `expr $end - $start` seconds.



echo "tallinn"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":2,"room_nr":2}' outfile.txt

end=`date +%s`
echo Execution time was `expr $end - $start` seconds.




echo "tallinn"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":2,"room_nr":3}' outfile.txt

end=`date +%s`
echo Execution time was `expr $end - $start` seconds.



echo "tallinn"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":2,"room_nr":4}' outfile.txt

end=`date +%s`
echo Execution time was `expr $end - $start` seconds.


echo "tallinn"
echo "2"
aws lambda invoke --cli-read-timeout 900 --function-name "$ENVIRONMENT-kv-ee-scraper"  --payload '{"city_name":"tallinn","deal_type":2,"room_nr":5}' outfile.txt

end=`date +%s`
echo Execution time was `expr $end - $start` seconds.