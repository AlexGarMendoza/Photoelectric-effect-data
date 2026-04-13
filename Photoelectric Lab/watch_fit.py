import time
import importlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import analysis
import report_plots

WAVELENGTHS = [
    "1700A", "1800A", "1900A", "2000A", "2100A",
    "2200A", "2300A", "2400A", "2500A", "2600A", "2700A"
]


def rerun_all():
    importlib.reload(analysis)
    importlib.reload(report_plots)
    from report_plots import plot_photocurrent_curve, plot_final_fit
    for key in WAVELENGTHS:
        plot_photocurrent_curve(key, f"figure_photocurrent_{key}.png")
    plot_final_fit("figure_stopping_voltage.png")


class AnalysisHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith("analysis.py"):
            print("analysis.py changed — rerunning all figures...")
            try:
                rerun_all()
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    observer = Observer()
    observer.schedule(AnalysisHandler(), path=".", recursive=False)
    observer.start()
    print("Watching analysis.py — save to regenerate all figures. Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
