

echo "Pull data"
# docker cp pencarian:/dirPencarian/jsonSaved/unpulledJson/. <destinanation>
docker cp pencarian:/dirPencarian/jsonSaved/unpulledJson/. /home/vps/jsonExperiment/.


echo "delete pulled data"
sudo docker exec -i pencarian mv -v /dirPencarian/jsonSaved/unpulledJson /dirPencarian/jsonSaved/pulledJson/pulled$(date +'%FT%T') #dimove folder karena file di docker tidak resudgular
sudo docker exec -i pencarian mkdir /dirPencarian/jsonSaved/unpulledJson

