import sys
import os
import ConfigParser

class MyConfigParser( ConfigParser.ConfigParser ):
	def __init__(self,defaults=None):  
		ConfigParser.ConfigParser.__init__(self,defaults=None)  
	def optionxform(self, optionstr):  
		return optionstr  


class config_generator:
	def __init__( self, args ):
		self.m_args = args
		os.system( 'mkdir %s/etc'% self.m_args.base_dir)

	def generate_config( self ):
		ret = self.generate_mysql_config()
		if ret != 0:
			print 'generate_mysql_config failed,ret %d'%ret 
			return ret

		ret = self.generate_phxbinlogsvr_config()
		if ret != 0:
			print 'generate_phxbinlogsvr_config failed, ret %d'%ret
			return ret

		ret = self.generate_phxsqlproxy_config()
		if ret != 0:
			print 'generate_phxsqlproxy_config failed, ret %d'%ret
			return ret

		return 0

	def generate_mysql_config( self ):
		cp = MyConfigParser()
		cp.read( 'etc_template/my.cnf' )
		cp.set( 'mysqld', 'port', self.m_args.mysql_port )
		cp.set( 'mysqld', 'plugin-dir', '%s/lib'%self.m_args.base_dir )
		cp.set( 'mysqld', 'basedir', '%s/percona.src'%self.m_args.base_dir )
		cp.set( 'mysqld', 'datadir', '%s/percona.workspace/data'%self.m_args.data_dir )
		cp.set( 'mysqld', 'tmpdir', '%s/percona.workspace/tmp'%self.m_args.data_dir )
		cp.set( 'mysqld', 'socket', '%s/percona.workspace/tmp/percona.sock'%self.m_args.data_dir )
		cp.set( 'mysqld', 'log-error', '%s/percona.workspace/log.err'%self.m_args.data_dir )
		cp.set( 'mysqld', 'log-bin', '%s/percona.workspace/binlog/mysql-bin'%self.m_args.data_dir )
		cp.set( 'mysqld', 'relay-log', '%s/percona.workspace/binlog/relay-log'%self.m_args.data_dir )
		cp.set( 'mysqld', 'innodb_data_home_dir', '%s/percona.workspace/innodb'%self.m_args.data_dir )
		cp.set( 'mysqld', 'innodb_log_group_home_dir', '%s/percona.workspace/innodb'%self.m_args.data_dir )
		cp.set( 'mysqld', 'innodb_undo_directory', '%s/percona.workspace/innodb'%self.m_args.data_dir )
		cp.write( open( '%s/etc/my.cnf'%self.m_args.base_dir, 'w' ) )
		os.system( 'chmod 644 %s/etc/my.cnf'%self.m_args.base_dir )
		return 0

	def generate_phxsqlproxy_config( self ):
		cp = MyConfigParser()
		cp.read( 'etc_template/phxsqlproxy.conf' )
		cp.set( 'Server', 'IP', self.m_args.inner_ip )
		cp.set( 'Server', 'Port', self.m_args.phxsqlproxy_port )
		cp.set( 'Server', 'LogFilePath', '%s/log'%self.m_args.data_dir)
		cp.write( open('%s/etc/phxsqlproxy.conf'%self.m_args.base_dir, 'w' ) )

		return 0

	def generate_phxbinlogsvr_config( self ):
		cp = MyConfigParser()
		cp.read( "etc_template/phxbinlogsvr.conf" );

		cp.set( "Server", "IP", '%s'%self.m_args.inner_ip )
		cp.set( "Server", "Port", '%s'%self.m_args.phxbinlogsvr_port )
		cp.set( 'Server', 'LogFilePath', '%s/log'%self.m_args.data_dir)

		cp.set( "AgentOption", "AgentPort", '%d'%self.m_args.agent_port )
		cp.set( "AgentOption", "EventDataDir", '%s/phxbinlogsvr/event_data'%self.m_args.data_dir )

		cp.set( "PaxosOption", "PaxosLogPath", '%s/phxbinlogsvr/paxoslog'%self.m_args.data_dir )
		cp.set( "PaxosOption", "PaxosPort", '%d'%self.m_args.paxos_port )

		cp.write(open('%s/etc/phxbinlogsvr.conf'%self.m_args.base_dir, 'w'))

		return 0
