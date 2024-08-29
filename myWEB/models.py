from django.db import models

class dzTable(models.Model):  # 读者信息
    dzid = models.AutoField(primary_key=True)  # 读者ID
    psw = models.CharField(max_length=256)  # 读者密码
    xm = models.CharField(max_length=10)  # 姓名
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(dzTable, self).save(force_insert, force_update, using, update_fields)
     
from django.contrib.auth.hashers import make_password

class tsglyTable(models.Model):
    glyid = models.CharField(max_length=10, primary_key=True)  # 工号
    psw = models.CharField(max_length=256)  # 管理员密码
    xm = models.CharField(max_length=10)  # 姓名

    def save(self, *args, **kwargs):
        self.psw = make_password(self.psw)  # 保存前加密密码
        super(tsglyTable, self).save(*args, **kwargs)

class smTable(models.Model):  # 书目信息
    isbn = models.CharField(max_length=50, primary_key=True)  # ISBN号
    sm = models.CharField(max_length=50)  # 书名
    zz = models.CharField(max_length=50)  # 作者
    cbs = models.CharField(max_length=50)  # 出版社
    cbny = models.DateTimeField()  # 出版年月
    count = models.IntegerField(default=0)  # 书籍数量

class tsTable(models.Model):  # 图书信息
    tsid = models.AutoField(primary_key=True)  # 图书id
    isbn = models.ForeignKey(smTable, on_delete=models.CASCADE)  # ISBN号
    cfwz = models.CharField(max_length=20)  # 存放位置（流通室、阅览室）
    zt = models.CharField(max_length=20)  # 状态（未借出、已借出、不外借、预留）
    jbr = models.ForeignKey(tsglyTable, on_delete=models.CASCADE)  # 经办人

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        assert self.cfwz in ('流通室', '阅览室'), '存放位置必须是流通室或阅览室'
        assert self.zt in ('未借出', '已借出', '不外借'), '图书状态必须是未借出、已借出、不外借、预留'
        super(tsTable, self).save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):  # 出库触发
        assert self.zt != '已借出', '已借出的图书不允许出库'
        super(tsTable, self).delete(using, keep_parents)

from django.core.validators import MinValueValidator, MaxValueValidator

class BookReview(models.Model):  # 书评
    dzid = models.ForeignKey(dzTable, on_delete=models.CASCADE)
    isbn = models.ForeignKey(smTable, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.TextField(blank=True, null=True, max_length=300)
    comment_time = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("dzid", "isbn")
        
class jsTable(models.Model):  # 借书信息
    dzid = models.ForeignKey(dzTable, on_delete=models.PROTECT)  # 读者ID
    tsid = models.ForeignKey(tsTable, on_delete=models.SET_NULL, null=True)  # 图书ID
    jysj = models.DateTimeField()  # 借阅时间
    yhsj = models.DateTimeField()  # 应还时间
    ghsj = models.DateTimeField(blank=True, null=True)  # 归还时间
    is_valid = models.BooleanField(default=True)  # 记录的有效性

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        assert self.jysj < self.yhsj, '归还时间应该在借阅时间之后'
        super(jsTable, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        unique_together = ("dzid", "tsid", "jysj")