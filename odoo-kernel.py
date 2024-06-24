from ipykernel.kernelbase import Kernel
import pexpect

CONTAINER_NAME = ''
DB_NAME = ''
DB_HOST = ''
DB_PORT = 5432
DB_USERNAME = 'odoo'
DB_PASSWORD = 'odoo'

odoo_command = f'docker exec -it {CONTAINER_NAME} odoo shell -d {DB_NAME} --db_host {DB_HOST} --db_port {DB_PORT} --db_user {DB_USERNAME} --db_password {DB_PASSWORD} --no-http'
odoo = None

class OdooKernel(Kernel):
    implementation = 'Odoo Kernel'
    implementation_version = '1.0'
    language = 'python'
    language_version = '3.9'
    language_info = {
        'name': 'Odoo Kernel',
        'mimetype': 'text/plain',
        'extension': '.py'
    }
    banner = "Odoo Kernel"
    odoo = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.odoo = pexpect.spawn(odoo_command)
        self.odoo.expect('>>> ')

    def __del__(self, **kwargs):
        super().__del__(**kwargs)

        self.odoo.sendline('exit()')
        self.odoo.close()
        self.odoo = None

    def do_execute(self, code, silent,
                   store_history=True,
                   user_expressions=None,
                   allow_stdin=False):

        if not silent:
            self.odoo.sendline(code)
            self.odoo.expect('>>> ')
            data = '\n'.join(self.odoo.before.decode('utf-8').splitlines()[1:])
            content = {
                'execution_count': self.execution_count,
                'data': {
                    'text/plain': data,
                },
                'metadata' : {}
            }
            self.send_response(self.iopub_socket, 'execute_result', content)

        return {
            'status': 'ok',
            'execution_count':
                self.execution_count,
            'payload': [],
            'user_expressions': {},
        }

if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp

    IPKernelApp.launch_instance(kernel_class=OdooKernel)


