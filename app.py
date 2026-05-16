import streamlit as st
import numpy as np
import plotly.graph_objects as go
import io
import wave

st.set_page_config(page_title="AngelMath", page_icon="👼", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&family=Space+Mono:wght@400;700&family=Poppins:wght@400;600&display=swap');

.stApp {
    background: radial-gradient(circle at top, #2b0018 0%, #080008 45%, #000000 100%);
    color: #ffe1f2;
    font-family: 'Poppins', sans-serif;
}

h1 {
    font-family: 'Orbitron', sans-serif;
    color: #ff4fc3;
    text-align: center;
    font-size: 4.4rem;
    text-shadow: 0 0 24px #ff1493;
    margin-bottom: 0.2rem;
}

.creator {
    text-align: center;
    color: #ffb6df;
    font-size: 0.95rem;
    letter-spacing: 1px;
    margin-bottom: 20px;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080008, #16000d);
    border-right: 1.5px solid #ff4fc3;
}

.equation-panel {
    background: linear-gradient(135deg, rgba(15,0,10,0.96), rgba(45,0,30,0.88));
    border: 1.5px solid #ff4fc3;
    border-radius: 24px;
    padding: 24px;
    margin: 20px 0 28px 0;
    box-shadow: 0 0 28px rgba(255, 20, 147, 0.65);
}

.equation-title {
    font-family: 'Orbitron', sans-serif;
    color: #ff8ada;
    font-size: 1.45rem;
    margin-bottom: 14px;
}

.math-line {
    font-family: 'Space Mono', monospace;
    color: #fff0f8;
    background-color: #080008;
    border-radius: 14px;
    padding: 16px;
    font-size: 1rem;
    line-height: 1.8;
    border: 1px solid #ff4fc3;
    box-shadow: inset 0 0 14px rgba(255, 79, 195, 0.25);
}

.description {
    color: #ffd1ec;
    font-size: 1rem;
    margin-top: 15px;
    line-height: 1.65;
}

.stDownloadButton button {
    background: linear-gradient(90deg, #ff1493, #ff69b4);
    color: white;
    border-radius: 14px;
    border: none;
    font-weight: 600;
    box-shadow: 0 0 15px rgba(255, 20, 147, 0.55);
}

.footer {
    text-align: center;
    color: #ffb6df;
    margin-top: 18px;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<h1>AngelMath</h1>
<div class="creator">Developed by Isa • @entropyischaotic</div>
""", unsafe_allow_html=True)


def make_tone():
    sample_rate = 44100
    duration = 2.5
    t_audio = np.linspace(0, duration, int(sample_rate * duration), False)

    tone = (
        0.22 * np.sin(2 * np.pi * 220 * t_audio) +
        0.18 * np.sin(2 * np.pi * 330 * t_audio) +
        0.14 * np.sin(2 * np.pi * 440 * t_audio) +
        0.08 * np.sin(2 * np.pi * 660 * t_audio)
    )

    fade = np.linspace(0, 1, int(sample_rate * 0.2))
    tone[:len(fade)] *= fade
    tone[-len(fade):] *= fade[::-1]

    tone = tone / np.max(np.abs(tone))
    audio = (tone * 32767).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())

    return buffer.getvalue()


with st.sidebar:
    st.header("Controls")

    shape = st.selectbox(
        "Choose a graph:",
        [
            "Heart",
            "Angel Wings",
            "Star",
            "Rose Flower",
            "Galaxy Spiral",
            "Helix",
            "Butterfly",
            "Torus",
            "Mobius Strip",
            "Wave Grid",
            "DNA Helix"
        ]
    )

    points = st.slider("Detail level", 500, 12000, 5000)
    point_size = st.slider("Point size", 2, 9, 4)
    show_grid = st.radio("Grid style:", ["On", "Minimal"])

    st.subheader("Audio")
    st.audio(make_tone(), format="audio/wav")


t = np.linspace(0, 2 * np.pi, points)

if shape == "Heart":
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    z = 5 * np.sin(t)

    equation = "x = 16sin³(t),  y = 13cos(t) − 5cos(2t) − 2cos(3t) − cos(4t),  z = 5sin(t)"
    description = "A parametric heart curve. The sine term creates the rounded sides, while the cosine terms shape the upper dip and pointed bottom."

elif shape == "Angel Wings":
    t = np.linspace(-np.pi, np.pi, points)
    base = np.exp(np.cos(t)) - 2*np.cos(4*t) - np.sin(t/12)**5

    x1 = np.sin(t) * base
    y1 = np.cos(t) * base
    z1 = 3 * np.sin(2*t)

    x = np.concatenate([x1, -x1])
    y = np.concatenate([y1, y1])
    z = np.concatenate([z1, z1])

    equation = "x = ±sin(t)(e^cos(t) − 2cos(4t) − sin⁵(t/12)),  y = cos(t)(e^cos(t) − 2cos(4t) − sin⁵(t/12)),  z = 3sin(2t)"
    description = "A mirrored parametric curve. The ± symbol reflects the x-values to create two symmetrical wing-like halves."

elif shape == "Star":
    r = 1 + 0.75 * np.cos(5*t)
    x = r * np.cos(t)
    y = r * np.sin(t)
    z = np.sin(5*t)

    equation = "r = 1 + 0.75cos(5t),  x = rcos(t),  y = rsin(t),  z = sin(5t)"
    description = "A polar star curve. The cos(5t) term creates five repeating points, and the z-value adds vertical variation."

elif shape == "Rose Flower":
    r = np.sin(8*t)
    x = r * np.cos(t)
    y = r * np.sin(t)
    z = np.cos(8*t)

    equation = "r = sin(8t),  x = rcos(t),  y = rsin(t),  z = cos(8t)"
    description = "A rose curve. The number inside sin(8t) controls the petal repetition, while z lifts the petals into 3D."

elif shape == "Galaxy Spiral":
    t = np.linspace(0, 12*np.pi, points)
    x = t * np.cos(t)
    y = t * np.sin(t)
    z = 8 * np.sin(t)

    equation = "x = tcos(t),  y = tsin(t),  z = 8sin(t)"
    description = "An Archimedean spiral. As t increases, the radius grows, creating an expanding spiral structure."

elif shape == "Helix":
    t = np.linspace(0, 10*np.pi, points)
    x = np.cos(t)
    y = np.sin(t)
    z = t / 2

    equation = "x = cos(t),  y = sin(t),  z = t/2"
    description = "A helix. The x and y values move in a circle while z steadily increases, creating a coil."

elif shape == "Butterfly":
    base = np.exp(np.cos(t)) - 2*np.cos(4*t) - np.sin(t/12)**5
    x = np.sin(t) * base
    y = np.cos(t) * base
    z = np.sin(3*t)

    equation = "x = sin(t)(e^cos(t) − 2cos(4t) − sin⁵(t/12)),  y = cos(t)(e^cos(t) − 2cos(4t) − sin⁵(t/12)),  z = sin(3t)"
    description = "A butterfly curve. It combines exponential and trigonometric terms to form wing-like lobes."

elif shape == "Torus":
    u = np.linspace(0, 2*np.pi, int(np.sqrt(points)))
    v = np.linspace(0, 2*np.pi, int(np.sqrt(points)))
    u, v = np.meshgrid(u, v)

    R = 3
    r = 1

    x = ((R + r*np.cos(v)) * np.cos(u)).flatten()
    y = ((R + r*np.cos(v)) * np.sin(u)).flatten()
    z = (r * np.sin(v)).flatten()

    equation = "x = (R + rcos(v))cos(u),  y = (R + rcos(v))sin(u),  z = rsin(v)"
    description = "A torus. This is the mathematical form of a donut shape, built from two circular motions."

elif shape == "Mobius Strip":
    u = np.linspace(0, 2*np.pi, int(np.sqrt(points)))
    v = np.linspace(-0.5, 0.5, int(np.sqrt(points)))
    u, v = np.meshgrid(u, v)

    x = ((1 + v*np.cos(u/2)) * np.cos(u)).flatten()
    y = ((1 + v*np.cos(u/2)) * np.sin(u)).flatten()
    z = (v * np.sin(u/2)).flatten()

    equation = "x = (1 + vcos(u/2))cos(u),  y = (1 + vcos(u/2))sin(u),  z = vsin(u/2)"
    description = "A Möbius strip. It is a one-sided surface created by adding a half twist to a loop."

elif shape == "Wave Grid":
    side = int(np.sqrt(points))
    x_vals = np.linspace(-6, 6, side)
    y_vals = np.linspace(-6, 6, side)
    x, y = np.meshgrid(x_vals, y_vals)
    z = np.sin(x) * np.cos(y)

    x = x.flatten()
    y = y.flatten()
    z = z.flatten()

    equation = "z = sin(x)cos(y)"
    description = "A wave surface. The height z changes based on both x and y, creating repeating peaks and valleys."

elif shape == "DNA Helix":
    t = np.linspace(0, 10*np.pi, points)

    x1 = np.cos(t)
    y1 = np.sin(t)
    z1 = t / 3

    x2 = np.cos(t + np.pi)
    y2 = np.sin(t + np.pi)
    z2 = t / 3

    x = np.concatenate([x1, x2])
    y = np.concatenate([y1, y2])
    z = np.concatenate([z1, z2])

    equation = "strand 1: x = cos(t), y = sin(t), z = t/3;  strand 2: x = cos(t + π), y = sin(t + π), z = t/3"
    description = "A double helix model. Two spiral strands are offset by π radians, creating a DNA-like structure."


grid_color = "#3a0030" if show_grid == "On" else "#000000"

st.markdown(
    f"""
    <div class="equation-panel">
        <div class="equation-title">{shape} Equation</div>
        <div class="math-line">{equation}</div>
        <div class="description">{description}</div>
    </div>
    """,
    unsafe_allow_html=True
)

fig = go.Figure(data=[
    go.Scatter3d(
        x=x,
        y=y,
        z=z,
        mode="markers",
        marker=dict(
            size=point_size,
            color=z,
            colorscale="RdPu",
            opacity=0.92
        )
    )
])

fig.update_layout(
    title=f"{shape}",
    paper_bgcolor="#000000",
    plot_bgcolor="#000000",
    font=dict(color="#ffe1f2", family="Poppins"),
    scene=dict(
        bgcolor="#000000",
        xaxis=dict(color="#ff4fc3", gridcolor=grid_color),
        yaxis=dict(color="#ff4fc3", gridcolor=grid_color),
        zaxis=dict(color="#ff4fc3", gridcolor=grid_color),
    ),
    annotations=[
        dict(
            text="@entropyischaotic",
            x=0.5,
            y=0,
            xref="paper",
            yref="paper",
            showarrow=False,
            font=dict(size=14, color="rgba(255,182,223,0.55)")
        )
    ],
    margin=dict(l=0, r=0, b=0, t=40)
)

st.plotly_chart(fig, use_container_width=True)

st.download_button(
    label="Download graph as HTML",
    data=fig.to_html(),
    file_name=f"{shape.lower().replace(' ', '_')}_angelmath.html",
    mime="text/html"
)

st.markdown(
    """
    <div class="footer">
        github.com/entropyischaotic • Isa
    </div>
    """,
    unsafe_allow_html=True
)