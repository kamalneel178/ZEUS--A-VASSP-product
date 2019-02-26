import tensorflow as tf, sys
import os,time

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line in tf.gfile.GFile("/tf/output_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("/tf/output_graph.pb", 'rb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:    
	while True:
		if len(os.listdir('/root/md/'))!=0:
			for filename in os.listdir('/root/md/'):
				time.sleep(1)
				image_path = "/root/md/"+filename
				start=time.time()
				# Read in the image_data
				image_data = tf.gfile.FastGFile(image_path, 'rb').read()
				# Feed the image_data as input to the graph and get first prediction
				softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
				predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
				# Sort to show labels of first prediction in order of confidence
				top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
				for node_id in top_k:
					human_string = label_lines[node_id]
					score = predictions[0][node_id]
					net=(('%s (score = %.5f)' % (human_string, score)))
					if score>0.8:
						print net ," --> " ,filename
						print (time.time()-start)
				os.remove("/root/md/"+filename)
		else: continue
