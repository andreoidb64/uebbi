# Embedded file name: reboot.py
# 20160308 andreoidb64: +devel options (swith on/off FTP and telnet)
import runtime
import config
import os
import manager
from widgets import pyapp
from widgets.widget import SoftButtonContainer
from widgets.scrollview import SimpleUniformList
from widgets.ulist import UListTextItem
if config.target:
	PROFILE_PATH = '/root/.profile'
else:
	PROFILE_PATH = '~/.uebbi_profile'

class Main(pyapp.PyApp):
	name = 'reboot'

	def __init__(self, *args, **kwds):
		print ''
		print 'KWDS'
		print kwds
		print ''
		print ''
		print 'args'
		print args
		print ''
		print ''
		pyapp.PyApp.__init__(self)
		main_win = Reboot_MainView(self)
		self.add_window(main_win)


class Reboot_MainView(pyapp.Window):
	"""
	\xec\x84\xa4\xec\xa0\x95\xea\xb0\x92 \xec\xb4\x88\xea\xb8\xb0\xed\x99\x94 \xed\x95\x98\xeb\x8a\x94 window class
	"""

	def __init__(self, app):
		self.__super.__init__(app)
		self.set_title(_('U&B Utils'))
		btn_conf = {'right': (_('Back'), 'right')}
		self.soft_btn = SoftButtonContainer(self, btn_conf)
		self.soft_btn.add_callback('softbutton-clicked', self.cb_btn_back)
		self.make_list()

	def make_list(self):
		"""
		\xeb\xa6\xac\xec\x8a\xa4\xed\x8a\xb8 \xec\x83\x9d\xec\x84\xb1
		"""
		size = (runtime.app_width - 14, 160)
		sb_size = (49, 84)
		self.text_list = [_('Riavvia Uebbi'), _('Attiva opzioni sviluppatore'), _('Disattiva opzioni sviluppatore')]
		self._list = SimpleUniformList(self, (258, UListTextItem.item_height * 3), UListTextItem, self.text_list)
		sc_view = self._list.get_view()
		sc_view.pos = (35, 40 - runtime.indicator_height)
		self._list.add_callback('selected', self.selected)

	def selected(self, index):
		"""
		\xeb\xa6\xac\xec\x8a\xa4\xed\x8a\xb8 \xec\x84\xa0\xed\x83\x9d \xec\xb2\x98\xeb\xa6\xac
		"""
		if index == 0:
			self.cb_reboot()
		elif index == 1:
			self.start_ftp()
		elif index == 2:
			self.stop_ftp()

	def cb_reboot(self):
		"""
		factory reset callback
		"""

		def dialog_cb(result):
			if result == 0:
				self.user_reset(False)

		from widgets.dialog import YesNoDialog
		dialog = YesNoDialog('confirm', _('Riavvio Uebbi?'))
		dialog.add_callback('dialog-result', dialog_cb)

	def user_reset(self, user = True):
		"""
		\xec\x84\xa4\xec\xa0\x95\xea\xb0\x92 \xec\xb4\x88\xea\xb8\xb0\xed\x99\x94 \xeb\xb6\x80\xeb\xb6\x84
		"""
		manager.service.stop_all_services()
		os.system('/sbin/reboot')

	def start_ftp(self):

		def dialog_cb(result):
			if result == 0:
				self.ftp_on(False)

		from widgets.dialog import YesNoDialog
		dialog = YesNoDialog('confirm', _('Avvio opzioni sviluppatore?\nNON ATTIVARE se non sai\nesattamente a cosa serve!'))
		dialog.add_callback('dialog-result', dialog_cb)

	def ftp_on(self, user = True):
		from widgets.dialog import MessageDialog
		os.system('/usr/bin/tcpsvd -vE 0.0.0.0 21 /usr/sbin/ftpd -w / &')
		os.system('/usr/sbin/telnetd -p 23 &')
		dialog = MessageDialog('confirm', _('Opzioni sviluppatore avviate.\nRicordati di arrestarle una\nvolta terminate le modifiche!'))

	def stop_ftp(self):

		def dialog_cb(result):
			if result == 0:
				self.ftp_off(False)

		from widgets.dialog import YesNoDialog
		dialog = YesNoDialog('confirm', _('Vuoi disattivare le\nopzioni sviluppatore?'))
		dialog.add_callback('dialog-result', dialog_cb)

	def ftp_off(self, user = True):
		from widgets.dialog import MessageDialog
		os.system('/usr/bin/killall tcpsvd')
		dialog = MessageDialog('confirm', _('Opzioni sviluppatore disattivate.'))

	def cb_btn_back(self, menu):
		"""
		back button callback
		"""
		self.close()
