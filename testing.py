import subprocess
import pytest


def run_converter(xml_content):
    with open('test_config.xml', 'w') as f:
        f.write(xml_content)
    result = subprocess.run(['python', 'converter.py', 'test_config.xml'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()


def test_database_config():
    xml_input = '''<config>
        <comment>Конфигурация для системы управления базами данных</comment>
        <dict name="databaseConfig">
            <item name="host">localhost</item>
            <item name="port">5432</item>
            <item name="username">admin</item>
            <item name="password">secret</item>
            <dict name="settings">
                <item name="max_connections">100</item>
                <item name="timeout">30</item>
            </dict>
        </dict>
        <const name="defaultSchema">public</const>
        <compute name="defaultSchema"/>
    </config>'''

    expected_output = '''|# Конфигурация для системы управления базами данных #|
dict(host = localhost, port = 5432, username = admin, password = secret, settings = dict(max_connections = 100, timeout = 30))
def defaultSchema = public;
?{defaultSchema}'''

    output = run_converter(xml_input)
    assert output == expected_output


def test_web_app_config():
    xml_input = '''<config>
        <comment>Конфигурация для веб-приложения</comment>
        <dict name="webAppConfig">
            <item name="port">8080</item>
            <item name="host">0.0.0.0</item>
            <dict name="routes">
                <item name="home">/home</item>
                <item name="about">/about</item>
                <dict name="api">
                    <item name="getUser  ">/api/user</item>
                    <item name="getPosts">/api/posts</item>
                </dict>
            </dict>
        </dict>
        <const name="version">1.0.0</const>
        <compute name="version"/>
    </config>'''

    expected_output = '''|# Конфигурация для веб-приложения #|
dict(port = 8080, host = 0.0.0.0, routes = dict(home = /home, about = /about, api = dict(getUser   = /api/user, getPosts = /api/posts)))
def version = 1.0.0;
?{version}'''

    output = run_converter(xml_input)
    assert output == expected_output


if __name__ == '__main__':
    pytest.main()
