import tensorflow as tf, sys
import os,time,cv2

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line in tf.gfile.GFile("/tf/output_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("/tf/output_graph.pb", 'rb') as f:
	graph_def = tf.GraphDef()
	graph_def.ParseFromString(f.read())
	_ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:    
	while True:
		camera = cv2.VideoCapture(0)
		retval, im = camera.read()
		cv2.imwrite("pics.jpeg",im)
		cv2.imshow("pic",im)
		del(camera)
		if True:
				image_path = "pics.jpeg"
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
					#if score>0.7:
					print net
					print (time.time()-start)
				print "....................................................."
		else: continue
