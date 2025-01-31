# -*- coding: utf-8 -*-
# from odoo import http


# class VideoClub(http.Controller):
#     @http.route('/video_club/video_club', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/video_club/video_club/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('video_club.listing', {
#             'root': '/video_club/video_club',
#             'objects': http.request.env['video_club.video_club'].search([]),
#         })

#     @http.route('/video_club/video_club/objects/<model("video_club.video_club"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('video_club.object', {
#             'object': obj
#         })
