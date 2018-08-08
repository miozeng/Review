import face_recognition
mm_image = face_recognition.load_image_file("D:\\test2\\mm.jpg");
wz_image = face_recognition.load_image_file("D:\\test2\\wz.jpg");
unknown_image = face_recognition.load_image_file("D:\\test2\\C360.jpg");

mm_encoding = face_recognition.face_encodings(mm_image)[0]
wz_encoding = face_recognition.face_encodings(wz_image)[0]
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
print(unknown_encoding)

results = face_recognition.compare_faces([mm_encoding, wz_encoding], unknown_encoding)
labels = ['mio', 'coffee']

print('results:' + str(results))

for i in range(0, len(results)):
    if results[i] == True:
        print('The person is:' + labels[i])
