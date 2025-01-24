from django.db import models


class DeletedModel(models.Model):
    deleted = models.BooleanField(verbose_name="已删除", default=False)

    class Meta:
        abstract = True


class UserInfo(DeletedModel):
    """ 用户表 """
    username = models.CharField(verbose_name="用户名", max_length=32)
    phone = models.CharField(verbose_name="手机号", max_length=32, db_index=True)
    password = models.CharField(verbose_name="密码", max_length=64)

    token = models.CharField(verbose_name="token", max_length=64, null=True, blank=True, db_index=True)
    token_expiry_date = models.DateTimeField(verbose_name="token有效期", null=True, blank=True)

    status_choice = (
        (1, "激活"),
        (2, "禁用"),
    )
    status = models.IntegerField(verbose_name="状态", choices=status_choice, default=1)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        # The newer indexes option provides more functionality than index_together
        # index_together may be deprecated in the future.
        # https://docs.djangoproject.com/en/3.2/ref/models/options/#index-together
        indexes = [
            models.Index(fields=['username', "password"], name='idx_name_pwd')
        ]


class Topic(DeletedModel):
    """ 话题 """
    title = models.CharField(verbose_name="话题", max_length=16, db_index=True)

    is_hot = models.BooleanField(verbose_name="热门话题", default=False)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)


class News(DeletedModel):
    """ 新闻资讯 """
    zone_choices = ((1, "42区"), (2, "段子"), (3, "图片"), (4, "挨踢1024"), (5, "你问我答"))
    zone = models.IntegerField(verbose_name="专区", choices=zone_choices)

    title = models.CharField(verbose_name="文字", max_length=150)
    url = models.CharField(verbose_name="链接", max_length=200, null=True, blank=True)

    # xxxxx?xxxxxx.png,xxxxxxxx.jeg
    image = models.TextField(verbose_name="图片地址", help_text="逗号分割", null=True, blank=True)

    topic = models.ForeignKey(verbose_name="话题", to="Topic", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)

    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    status_choice = (
        (1, "待审核"),
        (2, "已通过"),
        (3, "未通过"),
    )
    status = models.IntegerField(verbose_name="状态", choices=status_choice, default=1)

    collect_count = models.IntegerField(verbose_name="收藏数", default=0)
    recommend_count = models.IntegerField(verbose_name="推荐数", default=0)
    comment_count = models.IntegerField(verbose_name="评论数", default=0)


class Collect(models.Model):
    """ 收藏 """
    news = models.ForeignKey(verbose_name="资讯", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        # unique_together = [['news', 'user']]
        constraints = [
            models.UniqueConstraint(fields=['news', 'user'], name='uni_collect_news_user')
        ]


class Recommend(models.Model):
    """ 推荐 """
    news = models.ForeignKey(verbose_name="资讯", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['news', 'user'], name='uni_recommend_news_user')
        ]


class Comment(models.Model):
    """ 评论表 """
    news = models.ForeignKey(verbose_name="资讯", to="News", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    content = models.CharField(verbose_name="内容", max_length=150)

    depth = models.IntegerField(verbose_name="深度", default=0)

    root = models.ForeignKey(verbose_name="根评论", to="Comment", related_name="descendant", on_delete=models.CASCADE,
                             null=True, blank=True)

    reply = models.ForeignKey(verbose_name="回复", to="Comment", related_name="reply_list", on_delete=models.CASCADE,
                              null=True, blank=True)

    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    # 针对根评论
    descendant_update_datetime = models.DateTimeField(verbose_name="后代更新时间", auto_now_add=True)
