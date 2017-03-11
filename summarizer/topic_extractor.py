import metapy
import os
import shutil
from tokenizer import *


if __name__ == '__main__':
	if(os.path.exists('idx')):
		shutil.rmtree('idx')

	clean_document_and_return_sentances("Once upon a time there lived in a certain village a little country girl, the prettiest creature who was ever seen. Her mother was excessively fond of her; and her grandmother doted on her still more. This good woman had a little red riding hood made for her. It suited the girl so extremely well that everybody called her Little Red Riding Hood. One day her mother, having made some cakes, said to her, \"Go, my dear, and see how your grandmother is doing, for I hear she has been very ill. Take her a cake, and this little pot of butter.\" Little Red Riding Hood set out immediately to go to her grandmother, who lived in another village. As she was going through the wood, she met with a wolf, who had a very great mind to eat her up, but he dared not, because of some woodcutters working nearby in the forest. He asked her where she was going. The poor child, who did not know that it was dangerous to stay and talk to a wolf, said to him, \"I am going to see my grandmother and carry her a cake and a little pot of butter from my mother.\" \"Does she live far off?\" said the wolf \"Oh I say,\" answered Little Red Riding Hood; \"it is beyond that mill you see there, at the first house in the village.\" \"Well,\" said the wolf, \"and I\'ll go and see her too. I\'ll go this way and go you that, and we shall see who will be there first.\" The wolf ran as fast as he could, taking the shortest path, and the little girl took a roundabout way, entertaining herself by gathering nuts, running after butterflies, and gathering bouquets of little flowers. It was not long before the wolf arrived at the old woman\'s house. He knocked at the door: tap, tap. \"Who\'s there?\" \"Your grandchild, Little Red Riding Hood,\" replied the wolf, counterfeiting her voice; ")
	idx = metapy.index.make_inverted_index('config.toml')
	num_results = idx.num_docs()
	print num_results
	# Build the query object and initialize a ranker
	query = metapy.index.Document()
	ranker = metapy.index.OkapiBM25(k1=1.2,b=0.75,k3=500)

	query.content("shortest path")
	results = ranker.score(idx, query, num_results)
	print results                            


