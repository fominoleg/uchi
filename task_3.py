import numpy as np
import pandas as pd
import plotly.graph_objects as go


class BaseGraph:
    def __init__(self, data, title, x_title, y_title):
        if isinstance(data, pd.DataFrame):
            self.frame = data
        elif isinstance(data, str):
            self.frame = pd.read_csv(data)
        else:
            assert False, 'Некорректный параметр data'

        # self.data = data
        self.title = title
        self.x_title = x_title
        self.y_title = y_title

    def plot(self):
        layout = go.Layout(
            title=self.title,
            template="plotly_white",
            font=dict(
                size=18
            ),
            xaxis=dict(
                showgrid=True,
                showline=False,
                title=self.x_title,

            ),
            yaxis=dict(
                showgrid=True,
                title=self.y_title,
            )
        )
        fig = go.Figure(layout=layout)
        fig.add_trace(
            go.Scatter(x=self.frame[self.x_title], y=self.frame[self.y_title], mode='lines', name=self.title)
        )
        return fig


class BarGraph(BaseGraph):
    def plot(self):
        layout = go.Layout(
            title=self.title,
            template="plotly_white",
            font=dict(
                size=18
            ),
            xaxis=dict(
                showgrid=True,
                showline=False,
                title=self.x_title,

            ),
            yaxis=dict(
                showgrid=True,
                title=self.y_title,
            )
        )
        fig = go.Figure(layout=layout)
        fig.add_trace(
            go.Histogram(
                x=self.frame[self.x_title],
                y=self.frame[self.y_title],
                xbins=dict(
                    size=0.01
                ),
                ybins=dict(size=0.01),
                name=self.title,
            )
        )
        return fig


x = sorted(np.random.sample(100))
y = sorted(np.random.sample(100))
data = pd.DataFrame({'x': x, 'y': y})

bg = BaseGraph(data, 'BaseGraph', 'x', 'y')
fig = bg.plot()
fig.show()


bg = BarGraph(data, 'BarGraph', 'x', 'y')
fig = bg.plot()
fig.show()