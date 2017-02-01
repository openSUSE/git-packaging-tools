from gfp import get_diff_contents, unique


class TestUtils(object):
    '''
    Grouped tests for utility functions
    '''
    diff_a = """
From b338b21fe340ee4efa0045894315fcf20be1dc49 Mon Sep 17 00:00:00 2001
From: Test <info@suse.com>
Date: Wed, 14 Dec 2016 10:33:39 +0100
Subject: [PATCH] Avoid failures on SLES 12 SP2 because of new systemd
 TaskMax limit (bsc#985112)

---
 pkg/salt-master.service | 1 +
 1 file changed, 1 insertion(+)

diff --git a/pkg/salt-master.service b/pkg/salt-master.service
index 59be50301a..ecd3edd467 100644
--- a/pkg/salt-master.service
+++ b/pkg/salt-master.service
@@ -6,6 +6,7 @@ After=network.target
 LimitNOFILE=16384
 Type=simple
 ExecStart=/usr/bin/salt-master
+TasksMax=infinity

 [Install]
 WantedBy=multi-user.target
--
2.11.0
    """

    diff_b = """
From 7bbbd3b6ebaf3988a4f97b905040b56be065f201 Mon Sep 17 00:00:00 2001
From: Test <info@suse.com>
Date: Fri, 29 Jul 2016 10:50:21 +0200
Subject: [PATCH] Run salt-api as user salt (bsc#990029)

---
 pkg/salt-api.service | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)

diff --git a/pkg/salt-api.service b/pkg/salt-api.service
index c3e67d510c..9be2cb8ee6 100644
--- a/pkg/salt-api.service
+++ b/pkg/salt-api.service
@@ -3,8 +3,8 @@ Description=The Salt API
 After=network.target

 [Service]
-Type=notify
-NotifyAccess=all
+User=salt
+Type=simple
 LimitNOFILE=8192
 ExecStart=/usr/bin/salt-api
 TimeoutStopSec=3
--
2.11.0
    """

    diff_c = """
From 0943872fab17ae5400acc5b66cdb338193291e9e Mon Sep 17 00:00:00 2001
From: Test <info@saltstack.com>
Date: Mon, 30 Jan 2017 16:43:40 -0700
Subject: [PATCH 350/351] Add 2016.11.3 release notes file (#39044)

---
 doc/topics/releases/2016.11.3.rst | 5 +++++
 1 file changed, 5 insertions(+)
 create mode 100644 doc/topics/releases/2016.11.3.rst

diff --git a/doc/topics/releases/2016.11.3.rst b/doc/topics/releases/2016.11.3.rst
new file mode 100644
index 0000000000..cb2a5974ff
--- /dev/null
+++ b/doc/topics/releases/2016.11.3.rst
@@ -0,0 +1,5 @@
+============================
+Salt 2016.11.3 Release Notes
+============================
+
+Version 2016.11.3 is a bugfix release for :ref:`2016.11.0 <release-2016-11-0>`.
--
2.11.0
    """

    def test_get_diff_contents(self):
        '''
        Test diff content extracted properly.
        :return:
        '''
        sample_content_a = [' LimitNOFILE=16384\n Type=simple\n ExecStart=/usr/bin/salt-master'
                           '\n+TasksMax=infinity\n\n [Install]\n WantedBy=multi-user.target\n']
        assert get_diff_contents(self.diff_a) == sample_content_a

        sample_content_b = [' After=network.target\n\n [Service]\n-Type=notify\n-NotifyAccess=all'
                            '\n+User=salt\n+Type=simple\n LimitNOFILE=8192\n ExecStart=/usr/bin/salt-api'
                            '\n TimeoutStopSec=3\n']
        assert get_diff_contents(self.diff_b) == sample_content_b

        sample_content_c = ['+============================\n+Salt 2016.11.3 Release Notes\n'
                            '+============================\n+\n+Version 2016.11.3 is a bugfix release '
                            'for :ref:`2016.11.0 <release-2016-11-0>`.\n']
        assert get_diff_contents(self.diff_c) == sample_content_c

    def test_make_unique_filename(self):
        '''
        Test unique filename
        :return:
        '''
        fname = 'file.patch'
        for iter in xrange(10):
            fname = unique(fname)
            assert fname == 'file-{0}.patch'.format(iter + 1)

        fname = 'file-something.patch'
        for iter in xrange(10):
            fname = unique(fname)
            assert fname == 'file-something-{0}.patch'.format(iter + 1)

        fname = 'some-archive-here.tar.gz'
        for iter in xrange(10):
            fname = unique(fname)
            assert fname == 'some-archive-here-{0}.tar.gz'.format(iter + 1)
