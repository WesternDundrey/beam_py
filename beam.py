# beam.py

import numpy as np
import plotly.graph_objs as go

class Beam:
    def __init__(self, length=10, load=500, load_position=None, support='simply_supported'):
        self.length = length
        self.load = load
        self.load_position = load_position if load_position is not None else length / 2
        self.support = support

    def calculate_reactions(self):
        if self.support == 'simply_supported':
            R1 = self.load * (self.length - self.load_position) / self.length
            R2 = self.load * self.load_position / self.length
            return R1, R2
        elif self.support == 'cantilever':
            R = self.load
            M = self.load * (self.length - self.load_position)
            return R, M
        else:
            raise ValueError("Unsupported support type.")

    def shear_force(self):
        x = np.linspace(0, self.length, 100)
        V = np.zeros_like(x)
        if self.support == 'simply_supported':
            R1, _ = self.calculate_reactions()
            V = np.where(x < self.load_position, R1, R1 - self.load)
        elif self.support == 'cantilever':
            V = np.where(x < self.load_position, self.load, 0)
        return x, V

    def bending_moment(self):
        x = np.linspace(0, self.length, 100)
        M = np.zeros_like(x)
        if self.support == 'simply_supported':
            R1, _ = self.calculate_reactions()
            M = np.where(
                x < self.load_position,
                R1 * x,
                R1 * x - self.load * (x - self.load_position)
            )
        elif self.support == 'cantilever':
            M = np.where(
                x < self.load_position,
                self.load * (self.length - x),
                0
            )
        return x, M

    def deflection(self, E=200e9, I=1e-6):
        x = np.linspace(0, self.length, 100)
        delta = np.zeros_like(x)
        if self.support == 'simply_supported':
            a = self.load_position
            b = self.length - a
            L = self.length
            P = self.load
            EIL = E * I * L
            for i, xi in enumerate(x):
                if xi <= a:
                    delta[i] = (P * b * xi * (L**2 - b**2 - xi**2)) / (6 * EIL)
                else:
                    delta[i] = (P * b * (L - xi) * (2 * L * xi - xi**2 - b**2)) / (6 * EIL)
        elif self.support == 'cantilever':
            a = self.load_position
            L = self.length
            P = self.load
            EI = E * I
            for i, xi in enumerate(x):
                if xi <= a:
                    delta[i] = (P * (L - a) * xi**2) / (2 * EI)
                else:
                    delta[i] = (P * (L - a) * (2 * xi * (L - xi) - (L - a)**2)) / (2 * EI)
        return x, delta

    def plot_beam(self):
        """
        Creates a simple 2D render of the beam with supports and load.
        Returns a Plotly figure object.
        """
        # Beam representation
        beam_line = go.Scatter(
            x=[0, self.length],
            y=[0, 0],
            mode='lines',
            line=dict(color='saddlebrown', width=10),
            hoverinfo='none',
            showlegend=False
        )

        # Supports
        support_shapes = []
        annotations = []

        if self.support == 'simply_supported':
            # Left support (roller)
            support_shapes.append(dict(
                type='path',
                path='M 0,0 L -0.5,-0.5 L 0.5,-0.5 Z',
                fillcolor='gray',
                line=dict(color='gray')
            ))
            # Right support (pin)
            support_shapes.append(dict(
                type='path',
                path=f'M {self.length},0 L {self.length - 0.5},-0.5 L {self.length + 0.5},-0.5 Z',
                fillcolor='gray',
                line=dict(color='gray')
            ))
        elif self.support == 'cantilever':
            # Fixed support at x=0
            support_shapes.append(dict(
                type='rect',
                x0=-0.5,
                y0=-1,
                x1=0,
                y1=1,
                fillcolor='gray',
                line=dict(color='gray')
            ))

        # Load arrow
        load_arrow = go.Scatter(
            x=[self.load_position],
            y=[0],
            mode='markers',
            marker=dict(
                symbol='arrow-bar-down',
                size=20,
                color='red'
            ),
            hoverinfo='none',
            showlegend=False
        )

        annotations.append(dict(
            x=self.load_position,
            y=-1,
            xref='x',
            yref='y',
            text=f'Load = {self.load} N',
            showarrow=False,
            yshift=-10,
            font=dict(color='red')
        ))

        layout = go.Layout(
            shapes=support_shapes,
            xaxis=dict(range=[-1, self.length + 1], showgrid=False, zeroline=False, visible=False),
            yaxis=dict(range=[-2, 2], showgrid=False, zeroline=False, visible=False),
            height=200,
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=annotations
        )

        fig = go.Figure(data=[beam_line, load_arrow], layout=layout)
        return fig

    def plot_shear_force(self):
        x, V = self.shear_force()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=V, fill='tozeroy', name='Shear Force', line=dict(color='blue')))
        fig.update_layout(title='Shear Force Diagram', xaxis_title='Position along the beam (m)', yaxis_title='Shear Force (N)')
        return fig

    def plot_bending_moment(self):
        x, M = self.bending_moment()
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=M, fill='tozeroy', name='Bending Moment', line=dict(color='red')))
        fig.update_layout(title='Bending Moment Diagram', xaxis_title='Position along the beam (m)', yaxis_title='Bending Moment (Nm)')
        return fig

    def plot_deflection(self, E=200e9, I=1e-6):
        x, delta = self.deflection(E, I)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=delta * 1e3, name='Deflection', line=dict(color='green')))
        fig.update_layout(title='Deflection Curve', xaxis_title='Position along the beam (m)', yaxis_title='Deflection (mm)')
        return fig
