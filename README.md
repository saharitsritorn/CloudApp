# Project-Cloud-App 
## member
* นายนันท์ธร วงษ์ชมภู รหัสนักศึกษา 623040267-4
* นายปฏิภาณ นาชะนาง รหัสนักศึกษา 623040272-1
* นายสหฤทธิ์ ศรีธร รหัสนักศึกษา 623040338-7 
* นายทวัตถ์ เกียรตินิรันดร์ รหัสนักศึกษา 623040439-1 
## service
* **ml** <br> เป็น flask ที่จะเรียก script  ตัว แยกเสียงแยกได้สองคนเท่านั้น pretrain model ที่ใช้มี
    * sepformer-wsj02mix ของ speechbrain ใช้แยกเสียงพูดเมื่อคนพูดทับกัน
    * speaker-diarization  ของ pyannote ใช้แบ่งจังหวะเสียงพูด
    * whisper  ของ openai ใช้ แปลงเสียงเป็น text 
    > ในscript flask จะมีการเรียก script ที่จะทำการประมวลผล ไฟล์เสียง example.wav
    > <br>โดยจะเรียกแยก thread แยกกับตัว flask ตัวflask จะมี 2 route คือ 
    > * <ml:5000/> จะเป็น route ที่จะreturn string "Please wait while the audio is being processed." เมื่อ ยังประมวลผมไม่เสร็จ และreturnผลลัพธ์ model เมื่อ ประมวลผมเสร็จ(cpu 5800x ใช้เวลาประมาณ 15 นาที กับ example audio(example.wav)ที่ยาวประมาณ 1.3 นาที)
    > * <ml:5000/example> จะเป็น route ที่จะreturn ผมลัพของ model

* **nginx** 
<br>ใช้ nginxเป็นเราเตอร์ในเซิร์ฟเวอร์ front-end และ node.js รวมถึงเซิร์ฟเวอร์ HTTP เพื่อส่ง react front-end 
* **api**
<br> จะเป็น back-end สำหรับ login จะประกอบไปด้วย  
    * express.js
    * CORS
* **client**
<br> front-end React +javascript
<br> มี bug ที่javascript(/CloudApp/client/public/index.html:บรรทัด211) ไม่สามารถดึงget api ของ **ml:5000/example** ได้ แต่ลองใช้ curl จาก **client** ไป get **ml:5000** แล้วได้ผลลัพธ์ของ model ตามที่คิดไว้

* **adminer**
<br> เป็น interface ไว้ interact กับ MySQL server
    

* **mysql_db**
<br> เป็น database สำหรับ ใส่ชื่อ กับ email 