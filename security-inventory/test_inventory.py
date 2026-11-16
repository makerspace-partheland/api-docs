import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec=importlib.util.spec_from_file_location('inventory',Path(__file__).with_name('inventory.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class InventoryTests(unittest.TestCase):
    def setUp(self):
        m.action_versions.cache_clear()

    def test_pinned_commit_resolves_only_its_real_version_tags(self):
        tags=[{'name':'v7','commit':{'sha':'a'*40}}, {'name':'v7.0.1','commit':{'sha':'a'*40}},
              {'name':'v7.0.2','commit':{'sha':'b'*40}}]
        with patch.object(m,'api',return_value=tags):
            self.assertEqual(m.action_versions('actions/checkout','a'*40),['7.0.1'])
            self.assertEqual(m.action_versions('actions/checkout','v7'),['7.0.1'])
            self.assertEqual(m.action_versions('actions/checkout','c'*40),[])

    def test_workflow_data_does_not_become_a_command(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'example.yml').write_text('uses: actions/checkout@'+'a'*40+' # v7\n  - uses: "docker/login-action@v4.8.0"\n  uses: ./local\n  uses: ${{ matrix.action }}\n')
            self.assertEqual(m.action_references(p),[('actions/checkout','a'*40),('docker/login-action','v4.8.0')])

    def test_advisories_cover_reviewed_and_malware_without_duplicates(self):
        finding={'ghsa_id':'GHSA-test','cve_id':'CVE-2099-1234','severity':'high','summary':'synthetic',
                 'type':'reviewed','html_url':'https://github.com/advisories/GHSA-test','vulnerabilities':[]}
        with patch.object(m,'api',return_value=[finding]) as api:
            values=m.affected('npm',['swagger-ui@5.0.1'])
            self.assertEqual(len(values),1)
            self.assertIn('type=reviewed',api.call_args_list[0].args[0])
            self.assertIn('type=malware',api.call_args_list[1].args[0])
            self.assertIn('affects=swagger-ui%405.0.1',api.call_args_list[0].args[0])

    def test_api_failure_is_not_a_clean_empty_report(self):
        with patch.object(m,'api',side_effect=RuntimeError('permission denied')):
            with self.assertRaisesRegex(RuntimeError,'permission denied'):
                m.affected('actions',['actions/checkout@7.0.1'])

if __name__=='__main__':unittest.main()
