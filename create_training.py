#usr/bin/python
import click

@click.command()
@click.option('-t',default='S',help='Type of the workout: [S]teady or [I]ntervals')
@click.option('-d',help='Duration of the specific segment in minutes')
@click.option('-p',help='Power on specific segment (%of FTP)')
@click.option('-c',default='0',help="Cadence (RPM)")
def cli(type, duration, power, cadence):
    click.echo(type,duration)
    click.echo("sss")