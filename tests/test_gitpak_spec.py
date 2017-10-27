from gpak import SpecProcess
from mock import MagicMock, patch, mock_open


class TestSpecProcess(object):
    '''
    Tests SpecProcess class methods.
    '''
    @patch('os.path.dirname', MagicMock())
    @patch('os.path.basename', MagicMock())
    @patch('spec.Spec.from_file', MagicMock())
    def test_extract_message_conditions(self):
        text_top = '''@@osc-pkg-cond:0%{?rhel} == 6 || 0%{?suse_version} == 1110
Lorem ipsum dolor sit amet, mea discere oporteat eleifend te.
In solum utamur imperdiet mel, agam homero viderer cu sed,
malis liber deserunt cu his. Eu elit meis cum, pri te laoreet
oportere expetendis. Ne dicant maluisset usu.'''
        text_middle = '''Lorem ipsum dolor sit amet, mea discere
oporteat eleifend te. In solum utamur imperdiet mel,
agam homero viderer cu sed, malis liber deserunt cu his.
@@osc-pkg-cond:0%{?rhel} == 6 || 0%{?suse_version} == 1110
Eu elit meis cum, pri te laoreet oportere expetendis.
Ne dicant maluisset usu.'''
        text_end = '''Lorem ipsum dolor sit amet, mea discere
oporteat eleifend te. In solum utamur imperdiet mel,
agam homero viderer cu sed, malis liber deserunt cu his.
Eu elit meis cum, pri te laoreet oportere expetendis.
Ne dicant maluisset usu.
@@osc-pkg-cond:0%{?rhel} == 6 || 0%{?suse_version} == 1110'''
        _open = mock_open()
        with patch('gpak.open', _open, create=True):
            spec_process = SpecProcess(config={'spec': {}}, log=MagicMock())
            for text in [text_top, text_middle, text_end]:
                text, conditions = spec_process.extract_message_conditions(text=text)
                assert 'Lorem ipsum dolor sit amet' in text
                assert 'suse_version' not in text
                assert 'suse_version' in conditions
                assert 'rhel' in conditions
                assert '@@osc-pkg-cond:' not in conditions
                assert '@@osc-pkg-cond:' not in text
                assert conditions == '0%{?rhel} == 6 || 0%{?suse_version} == 1110'
