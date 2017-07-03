import pymysql


connection = None



class VideoInfo(object) :
	'''
	Video database handle.
	'''
	def __init__(self, i_id) :
		self.id = i_id

	def __str__(self) :
		return '(VideoInfo[%s]:<%s>)' % (self.get_id(), self.get_name())

	def __repr__(self) :
		return self.__str__()

	def get_id(self) :
		'''
		Returns video's id.
		'''
		return self.id

	def get_name(self) :
		'''
		Returns video's name.
		'''
		with connection.cursor() as cursor :
			sql = "SELECT name FROM videos_info where id = %s"
			cursor.execute(sql, (self.get_id()))
			return cursor.fetchone()["name"]

	def get_parts(self) :
		'''
		Returns video's parts' info.
		'''
		with connection.cursor() as cursor :
			sql = "SELECT id FROM parts_info where video_id = %s ORDER BY order_number ASC"
			cursor.execute(sql, (self.get_id()))
			result = []
			for r in cursor.fetchall() :
				result.append(PartInfo(r["id"]))
			return result
			
	def count_parts(self) :
		'''
		Returns video's number of parts.
		'''
		with connection.cursor() as cursor :
			sql = "SELECT COUNT(*) FROM parts_info where video_id = %s"
			cursor.execute(sql, (self.get_id()))
			return cursor.fetchone()["COUNT(*)"]

	def append_part(self, part_name) :
		'''
		Append a part to this video. Returns its info.
		'''
		with connection.cursor() as cursor :
			sql = "INSERT INTO parts_info(video_id, name, order_number) VALUES(%s, %s, %s)"
			cursor.execute(sql, (self.get_id(), part_name, self.count_parts() + 1))
		connection.commit()
		return PartInfo(get_last_id())



class PartInfo(object) :
	'''
	Part database handle.
	'''
	def __init__(self, i_id) :
		self.id = i_id

	def __str__(self) :
		return '(PartInfo[%s]:<%s>%s-%s.%s)' % (self.get_id(),
												self.get_video().get_id(),
												self.get_video().get_name(),
												self.get_order_num(),
												self.get_name())

	def __repr__(self) :
		return self.__str__()

	def get_id(self) :
		'''
		Return part's id.
		'''
		return self.id

	def get_name(self) :
		'''
		Return part's name.
		'''
		with connection.cursor() as cursor :
			sql = "SELECT name FROM parts_info where id = %s"
			cursor.execute(sql, (self.get_id()))
			return cursor.fetchone()["name"]

	def get_video(self) :
		'''
		Return info of the video this part belongs to.
		'''
		with connection.cursor() as cursor :
			sql = "SELECT video_id FROM parts_info where id = %s"
			cursor.execute(sql, (self.get_id()))
			return VideoInfo(cursor.fetchone()["video_id"])

	def get_order_num(self) :
		'''
		Returns part's order number.
		'''
		with connection.cursor() as cursor :
			sql = "SELECT order_number FROM parts_info where id = %s"
			cursor.execute(sql, (self.get_id()))
			return cursor.fetchone()["order_number"]




def conn_db() :
	'''
	Connect to database.
	'''
	global connection
	connection = pymysql.connect(host = 'localhost',
								 user = 'root',
								 password = '',
								 db = 'moviewer',
								 charset = 'utf8mb4',
								 cursorclass = pymysql.cursors.DictCursor)
	print("Database connected.")



def disconn_db() :
	'''
	Disconnect from database.
	'''
	global connection
	connection.close()
	print("Database disconnected.")

	
	
def get_last_id() :
	'''
	Returns last added video or part's info.
	'''
	with connection.cursor() as cursor :
		sql = "SELECT LAST_INSERT_ID()"
		cursor.execute(sql)
		return cursor.fetchone()["LAST_INSERT_ID()"]
	


def get_videos() :
	'''
	Returns all videos' info.
	'''
	with connection.cursor() as cursor :
		sql = "SELECT id FROM videos_info"
		cursor.execute(sql)
		result = []
		for r in cursor.fetchall() :
			result.append(VideoInfo(r["id"]))
		return result

		
		
def add_video(name) :
	'''
	Add a new video info to database. Returns its info.
	'''
	with connection.cursor() as cursor :
		sql = "INSERT INTO videos_info(name) VALUES(%s)"
		cursor.execute(sql, (name))
	connection.commit()
	return VideoInfo(get_last_id())
